"""
JWT token issuance with KCheck-specific claims.

Every access token must carry: `user_id`, `email`, `portal`,
`tenant_id`, `roles`. The portal claim is the input to Layer-1 RBAC
(BFF permission classes); the roles claim is the input to Layer-2
(`HasPermission`).

Two issuance paths:

    1. Password grant — `LoginView` uses
       `KCheckTokenObtainPairSerializer`, a thin subclass of simplejwt's
       built-in serializer that attaches claims in `get_token`.

    2. OTP grant — `OTPVerifyView` builds the token by hand via
       `build_tokens_for_user`, since there is no password to validate.

The `roles` claim is a flat list of role names — the full permissions
list is not stuffed into the token (keeps tokens small; permissions
are looked up server-side when `HasPermission` fires).
"""
from __future__ import annotations

from typing import Dict, List

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


def _user_roles_payload(user) -> List[str]:
    """Return the list of role names attached to this user."""
    if not user.is_authenticated:
        return []
    return list(
        user.role_assignments.select_related("role").values_list(
            "role__name", flat=True
        )
    )


def _attach_kcheck_claims(token, user) -> None:
    """Attach KCheck-specific claims to a simplejwt token in-place."""
    token["user_id"] = str(user.id)
    token["email"] = user.email
    token["portal"] = user.portal
    token["tenant_id"] = str(user.tenant_id) if user.tenant_id else None
    token["roles"] = _user_roles_payload(user)


class KCheckTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Drop-in replacement for simplejwt's pair serializer that adds the
    KCheck custom claims. Used by `LoginView` (password grant).
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        _attach_kcheck_claims(token, user)
        return token


def build_tokens_for_user(user) -> Dict[str, str]:
    """
    Issue (refresh, access) for `user` without a password challenge.

    Used by `OTPVerifyView`. Returns a dict with `access` and `refresh`
    serialised strings — same shape `TokenObtainPairSerializer.validate`
    returns, so views can pass it straight through.
    """
    refresh = RefreshToken.for_user(user)
    _attach_kcheck_claims(refresh, user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}
