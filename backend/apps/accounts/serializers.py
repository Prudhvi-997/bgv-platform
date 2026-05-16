"""
DRF serializers for the accounts app.

`LoginSerializer` is the `KCheckTokenObtainPairSerializer` from
`tokens.py` (re-exported for naming clarity at the URL conf layer).
"""
from __future__ import annotations

from rest_framework import serializers

from .models import OTPCode, Role, User
from .tokens import KCheckTokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """Public representation of a User — read-only via the auth surface."""

    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "portal",
            "tenant_id",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
            "roles",
        )
        read_only_fields = fields

    def get_roles(self, user: User):
        return list(
            user.role_assignments.select_related("role").values_list(
                "role__name", flat=True
            )
        )


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name", "portal", "permissions", "created_at")
        read_only_fields = fields


# Login = the JWT pair serializer with KCheck claims. Exposed under a
# semantic name so the URL conf reads naturally.
LoginSerializer = KCheckTokenObtainPairSerializer


class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.RegexField(regex=r"^\d{6}$")


__all__ = [
    "UserSerializer",
    "RoleSerializer",
    "LoginSerializer",
    "OTPRequestSerializer",
    "OTPVerifySerializer",
    "OTPCode",  # convenience re-export for tests
]
