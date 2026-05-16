"""
Permission classes — both layers of CLAUDE.md Part 4.3.

Layer 1 — Portal access control. One class per portal. The class
          inspects the JWT's `portal` claim. Five existing BFF files
          (`backend/bff/<portal>_bff/permissions.py`) re-implement the
          same check locally; that duplication is intentional and
          left in place — these here are the canonical versions that
          shared code (e.g. accounts views) can import.

Layer 2 — Feature access control. `HasPermission(perm_string)` is a
          factory that returns a `BasePermission` subclass checking
          whether any of the user's role assignments grants
          `perm_string`. Wildcard `"*"` is matched (platform_admin).
"""
from __future__ import annotations

from typing import Iterable, Type

from rest_framework.permissions import BasePermission


# --- Layer 1: portal-scoped session checks ----------------------------------


class _PortalSessionPermission(BasePermission):
    """Reject sessions whose JWT portal claim does not match."""

    portal: str = ""
    message: str = "This endpoint requires a portal-scoped session."

    def has_permission(self, request, view):
        token = getattr(request, "auth", None)
        if token is None:
            return False
        return getattr(token, "get", lambda *_: None)("portal") == self.portal


class IsOpsPortalUser(_PortalSessionPermission):
    portal = "ops"
    message = "This endpoint is restricted to Operations Portal sessions."


class IsClientPortalUser(_PortalSessionPermission):
    portal = "client"
    message = "This endpoint is restricted to Client Portal sessions."


class IsCandidatePortalUser(_PortalSessionPermission):
    portal = "candidate"
    message = "This endpoint is restricted to Candidate Portal sessions."


class IsVendorPortalUser(_PortalSessionPermission):
    portal = "vendor"
    message = "This endpoint is restricted to Vendor Portal sessions."


class IsAdminPortalUser(_PortalSessionPermission):
    portal = "admin"
    message = "This endpoint is restricted to Super Admin Portal sessions."


# --- Layer 2: feature-level permission check --------------------------------


def _token_roles(request) -> Iterable[str]:
    token = getattr(request, "auth", None)
    if token is None:
        return ()
    roles = getattr(token, "get", lambda *_: None)("roles")
    return tuple(roles or ())


def _resolve_role_permissions(role_names: Iterable[str]) -> set:
    """Look up the union of permissions for the given role names."""
    # Local import dodges circular import at module load (`models` imports
    # this module's siblings indirectly through `managers`).
    from .models import Role

    perms: set = set()
    if not role_names:
        return perms
    for role in Role.objects.filter(name__in=list(role_names)):
        perms.update(role.permissions or [])
    return perms


def HasPermission(required: str) -> Type[BasePermission]:
    """
    Build a permission class that allows the request iff the
    authenticated user holds at least one role whose permissions list
    contains `required` (or `"*"`).

    Usage:
        @permission_classes([IsAuthenticated, HasPermission("cases.view")])
        def get(self, request): ...
    """

    class _Has(BasePermission):
        message = f"Missing permission: {required}"

        def has_permission(self, request, view):
            if not getattr(request, "user", None) or not request.user.is_authenticated:
                return False
            role_names = _token_roles(request)
            perms = _resolve_role_permissions(role_names)
            return "*" in perms or required in perms

    _Has.__name__ = f"HasPermission_{required.replace('.', '_')}"
    return _Has
