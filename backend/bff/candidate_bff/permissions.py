"""
Layer 1 RBAC for the Candidate Portal BFF.

A session token whose `portal` claim is not `candidate` cannot reach
any endpoint mounted under this BFF (CLAUDE.md Part 4.3).
"""
from rest_framework.permissions import BasePermission


class IsCandidatePortalSession(BasePermission):
    """Reject any session that is not scoped to the Candidate Portal."""

    message = "This endpoint is restricted to Candidate Portal sessions."

    def has_permission(self, request, view):
        token = getattr(request, "auth", None)
        if token is None:
            return False
        return getattr(token, "get", lambda *_: None)("portal") == "candidate"
