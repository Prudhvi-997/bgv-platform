"""
Layer 1 RBAC for the Vendor Portal BFF.

A session token whose `portal` claim is not `vendor` cannot reach
any endpoint mounted under this BFF (CLAUDE.md Part 4.3).
"""
from rest_framework.permissions import BasePermission


class IsVendorPortalSession(BasePermission):
    """Reject any session that is not scoped to the Vendor Portal."""

    message = "This endpoint is restricted to Vendor Portal sessions."

    def has_permission(self, request, view):
        token = getattr(request, "auth", None)
        if token is None:
            return False
        return getattr(token, "get", lambda *_: None)("portal") == "vendor"
