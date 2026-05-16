"""
Tenant context middleware.

For every request that carries a verified Bearer JWT, push the token's
`tenant_id` claim into the request-scoped contextvar. The `TenantManager`
reads it on every ORM query (`apps.accounts.managers.TenantManager`).

The middleware does its own JWT verification rather than waiting for
DRF's `JWTAuthentication` because DRF auth runs inside the view, by
which time querysets may have already executed. Verifying twice (once
here, once in DRF) is acceptable overhead and keeps the rule "tenant
context is always available to managers" simple.
"""
from __future__ import annotations

import uuid
from typing import Optional

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from .tenant_context import reset_current_tenant, set_current_tenant


def _extract_bearer(request) -> Optional[str]:
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if not auth_header:
        return None
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]


def _parse_tenant_claim(token_str: str) -> Optional[uuid.UUID]:
    """Verify the JWT and return its `tenant_id` claim, or None."""
    try:
        token = AccessToken(token_str)
    except TokenError:
        return None
    raw = token.get("tenant_id")
    if not raw:
        return None
    try:
        return uuid.UUID(str(raw))
    except (ValueError, AttributeError):
        return None


class TenantContextMiddleware:
    """Push the JWT tenant claim into the contextvar for this request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant: Optional[uuid.UUID] = None
        token_str = _extract_bearer(request)
        if token_str:
            tenant = _parse_tenant_claim(token_str)

        ctx_token = set_current_tenant(tenant)
        try:
            response = self.get_response(request)
        finally:
            reset_current_tenant(ctx_token)
        return response
