"""
Layer 1 RBAC for the Super Admin Portal BFF.

A session token whose `portal` claim is not `admin` cannot reach
any endpoint mounted under this BFF (CLAUDE.md Part 4.3).
"""
from rest_framework.permissions import BasePermission


class IsAdminPortalSession(BasePermission):
    """Reject any session that is not scoped to the Super Admin Portal."""

    message = "This endpoint is restricted to Super Admin Portal sessions."

    def has_permission(self, request, view):
        token = getattr(request, "auth", None)
        if token is None:
            return False
        return getattr(token, "get", lambda *_: None)("portal") == "admin"
