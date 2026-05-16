"""Unit tests for the KCheck-specific JWT claims."""
import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.accounts.models import Role, UserRole
from apps.accounts.tokens import (
    KCheckTokenObtainPairSerializer,
    build_tokens_for_user,
)
from rest_framework_simplejwt.tokens import AccessToken


User = get_user_model()


def _decode_access(serialised_pair) -> AccessToken:
    # `serialised_pair` is either {"access": "...", "refresh": "..."} from
    # `build_tokens_for_user` or the dict returned by
    # `TokenObtainPairSerializer.validate()`.
    return AccessToken(serialised_pair["access"])


class JwtClaimsTests(TestCase):
    def setUp(self):
        self.tenant = uuid.uuid4()
        self.user = User.objects.create_user(
            email="claim@kpmg.in",
            password="changeme123",
            full_name="Claim User",
            portal="ops",
            tenant_id=None,
        )
        # Attach two roles.
        self.role_a = Role.objects.create(
            name="ops_reviewer", portal="ops", permissions=["cases.view"]
        )
        self.role_b = Role.objects.create(
            name="adjudicator", portal="ops", permissions=["cases.adjudicate"]
        )
        UserRole.objects.create(user=self.user, role=self.role_a)
        UserRole.objects.create(user=self.user, role=self.role_b)

    def test_password_grant_token_carries_all_claims(self):
        refresh = KCheckTokenObtainPairSerializer.get_token(self.user)
        # Access derives from refresh; both must carry the claims.
        access = AccessToken(str(refresh.access_token))
        self.assertEqual(access["user_id"], str(self.user.id))
        self.assertEqual(access["email"], self.user.email)
        self.assertEqual(access["portal"], "ops")
        self.assertIsNone(access["tenant_id"])
        self.assertCountEqual(access["roles"], ["ops_reviewer", "adjudicator"])

    def test_otp_grant_token_carries_all_claims(self):
        tokens = build_tokens_for_user(self.user)
        access = _decode_access(tokens)
        self.assertEqual(access["user_id"], str(self.user.id))
        self.assertEqual(access["email"], self.user.email)
        self.assertEqual(access["portal"], "ops")
        self.assertIsNone(access["tenant_id"])
        self.assertCountEqual(access["roles"], ["ops_reviewer", "adjudicator"])

    def test_tenant_id_serialised_when_present(self):
        client_user = User.objects.create_user(
            email="client@acme.com",
            password="changeme123",
            full_name="Client",
            portal="client",
            tenant_id=self.tenant,
        )
        tokens = build_tokens_for_user(client_user)
        access = _decode_access(tokens)
        self.assertEqual(access["tenant_id"], str(self.tenant))
        self.assertEqual(access["portal"], "client")
        self.assertEqual(access["roles"], [])

    def test_roles_reflects_user_role_assignments(self):
        # User with no roles should carry an empty list.
        bare = User.objects.create_user(
            email="bare@kpmg.in",
            password="changeme123",
            full_name="Bare",
            portal="ops",
        )
        access = _decode_access(build_tokens_for_user(bare))
        self.assertEqual(access["roles"], [])
