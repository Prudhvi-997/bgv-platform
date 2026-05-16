"""
Layer 1 RBAC for the Operations Portal BFF.

A session token whose `portal` claim is not `ops` cannot reach
any endpoint mounted under `/api/ops/`, regardless of the user's
domain-level permissions (CLAUDE.md Part 4.3).
"""
from rest_framework.permissions import BasePermission


class IsOpsPortalSession(BasePermission):
    """Reject any session that is not scoped to the Ops portal."""

    message = "This endpoint is restricted to Operations Portal sessions."

    def has_permission(self, request, view):
        token = getattr(request, "auth", None)
        if token is None:
            return False
        return getattr(token, "get", lambda *_: None)("portal") == "ops"
