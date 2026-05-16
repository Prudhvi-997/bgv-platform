"""
Model managers for the accounts app.

Two distinct managers live here:

    UserManager — Django's auth contract adapter for our email-as-username
                  custom User model. Provides create_user / create_superuser.

    TenantManager — default manager for every multi-tenant model in the
                    platform. Auto-filters by the current request's
                    tenant_id (see `tenant_context.py`) and raises
                    PermissionDenied if no tenant is set when a query
                    runs.

The TenantManager is exported from this module so that other apps
(`cases`, `verification`, `candidates`, …) can use it as their default
manager without re-implementing the contextvar plumbing.
"""
from __future__ import annotations

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import PermissionDenied
from django.db import models

from .tenant_context import get_current_tenant, is_unfiltered_mode


# --- Custom user manager (email-as-username) --------------------------------


class UserManager(BaseUserManager):
    """Custom manager for the email-based User model."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required for every User.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            # Candidates have no password — OTP-only login.
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("portal", "admin")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


# --- Tenant-scoped manager (CLAUDE.md RISK-02 enforcement) ------------------


class TenantQuerySet(models.QuerySet):
    """Marker queryset — extension point for tenant-aware methods."""


class TenantManager(models.Manager.from_queryset(TenantQuerySet)):
    """
    Default manager for multi-tenant models.

    Behaviour:
        - If tenant context is set: filter every query by `tenant_id`.
        - If `unfiltered_scope()` is active: return an unfiltered queryset.
        - Otherwise: raise PermissionDenied. This makes "forgot to set
          tenant" a loud, visible failure during development rather than
          a silent data-isolation breach in production.

    Escape hatch: `Model.objects.unfiltered()` returns a queryset that
    bypasses tenant filtering. Every call site needs review (CLAUDE.md
    RISK-02).
    """

    use_for_related_fields = True

    def get_queryset(self):
        base = super().get_queryset()
        if is_unfiltered_mode():
            return base
        tenant = get_current_tenant()
        if tenant is None:
            raise PermissionDenied(
                f"Tenant context required to query {self.model.__name__}. "
                "Either authenticate with a tenant-scoped token or wrap "
                "the call in unfiltered_scope() / Model.objects.unfiltered()."
            )
        return base.filter(tenant_id=tenant)

    def unfiltered(self) -> TenantQuerySet:
        """Bypass tenant filtering. Use deliberately."""
        return super().get_queryset()
