"""
Accounts domain models.

Two-layer RBAC (CLAUDE.md Part 4.3):
    Layer 1 — Portal access control, enforced by BFF permission classes.
              The `portal` claim on the JWT and `User.portal` field are
              the inputs.
    Layer 2 — Feature access control, enforced by `HasPermission(...)`
              against the user's `Role.permissions` JSON.

Tenant isolation (CLAUDE.md RISK-02):
    `User.tenant_id` is nullable — null means "internal KPMG user"
    (ops, admin). Client / candidate / vendor users carry a non-null
    `tenant_id`. `UserRole` and `OTPCode` inherit the user's tenant
    when relevant.

UUID primary keys throughout. MySQL stores these as `char(32)`.
"""
from __future__ import annotations

import secrets
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models, transaction
from django.utils import timezone

from .managers import UserManager


PORTAL_CHOICES = (
    ("ops", "Operations Portal"),
    ("client", "Client Portal"),
    ("candidate", "Candidate Portal"),
    ("vendor", "Vendor Portal"),
    ("admin", "Super Admin Portal"),
)


# --- User -------------------------------------------------------------------


class User(AbstractBaseUser, PermissionsMixin):
    """
    KCheck user — one row per identifiable principal.

    Notes:
        - Email is the login identifier; there is no `username` field.
        - `portal` pins the user to a single portal (no cross-portal users).
          A client HR who is also a candidate at another company would
          have two distinct User rows.
        - `tenant_id` is nullable: ops and platform admins are internal
          and have no tenant. Client / candidate / vendor users do.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    portal = models.CharField(max_length=16, choices=PORTAL_CHOICES)
    tenant_id = models.UUIDField(null=True, blank=True, db_index=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "portal"]

    class Meta:
        db_table = "accounts_user"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["portal"]),
            models.Index(fields=["tenant_id", "portal"]),
        ]

    def __str__(self) -> str:
        return f"{self.email} ({self.portal})"


# --- OTP --------------------------------------------------------------------

OTP_LIFETIME = timedelta(minutes=10)


def _generate_six_digit_code() -> str:
    """Generate a cryptographically secure 6-digit OTP."""
    # secrets.randbelow guarantees uniform distribution; format ensures
    # leading zeros are preserved.
    return f"{secrets.randbelow(1_000_000):06d}"


class OTPCode(models.Model):
    """
    One-time password issued to a Candidate Portal user.

    Lifecycle:
        - `generate_for_user(user)` invalidates all the user's prior
          unused OTPs and issues a fresh one. Caller is responsible for
          delivering the code (logged to stdout until the notifications
          app is wired up).
        - `verify_for_user(user, code)` returns True at most once per
          OTP and marks the row used. Expired or already-used OTPs
          return False.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otp_codes",
    )
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts_otp_code"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "is_used"]),
        ]

    def __str__(self) -> str:
        return f"OTP({self.user_id}, used={self.is_used})"

    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    def is_valid(self) -> bool:
        return not self.is_used and not self.is_expired()

    @classmethod
    @transaction.atomic
    def generate_for_user(cls, user) -> "OTPCode":
        """
        Invalidate prior unused OTPs for this user, then issue a fresh one.

        The invalidation is a defensive measure against OTP stockpiling
        (CLAUDE.md 6.3.7 — security around the OTP flow).
        """
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        return cls.objects.create(
            user=user,
            code=_generate_six_digit_code(),
            expires_at=timezone.now() + OTP_LIFETIME,
        )

    @classmethod
    @transaction.atomic
    def verify_for_user(cls, user, code: str) -> bool:
        """
        Return True if `code` matches an active OTP for `user` and mark
        that OTP used. False otherwise. Constant-time-ish comparison via
        `secrets.compare_digest` to dodge naive timing attacks.
        """
        try:
            otp = (
                cls.objects.select_for_update()
                .filter(user=user, is_used=False)
                .latest("created_at")
            )
        except cls.DoesNotExist:
            return False
        if otp.is_expired():
            otp.is_used = True
            otp.save(update_fields=["is_used"])
            return False
        if not secrets.compare_digest(otp.code, code):
            return False
        otp.is_used = True
        otp.save(update_fields=["is_used"])
        return True


# --- Roles & assignments ----------------------------------------------------


class Role(models.Model):
    """
    Named role pinned to a portal, carrying a JSON list of permissions.

    Permissions are dotted strings (e.g. `"cases.view"`). The wildcard
    `"*"` belongs to `platform_admin` only and is matched in
    `HasPermission` (see `permissions.py`).

    Roles are global (not tenant-scoped). The user-to-role binding
    (`UserRole`) is tenant-scoped.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    portal = models.CharField(max_length=16, choices=PORTAL_CHOICES)
    permissions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "accounts_role"
        ordering = ("portal", "name")
        constraints = [
            models.UniqueConstraint(
                fields=["name", "portal"], name="uniq_role_name_per_portal"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name}@{self.portal}"


class UserRole(models.Model):
    """
    Assignment of a Role to a User. Tenant-scoped because the same human
    may have different roles in different client tenants (rare, but the
    schema must accommodate it).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="role_assignments",
    )
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="assignments")
    tenant_id = models.UUIDField(null=True, blank=True, db_index=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assignments_made",
    )

    class Meta:
        db_table = "accounts_user_role"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role", "tenant_id"],
                name="uniq_user_role_per_tenant",
            ),
        ]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["tenant_id"]),
        ]

    def __str__(self) -> str:
        return f"{self.user_id} → {self.role.name}"
