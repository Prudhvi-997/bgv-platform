"""End-to-end view tests for /api/auth/ endpoints."""
import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import OTPCode, Role, UserRole


User = get_user_model()


class LoginViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "changeme123"
        self.user = User.objects.create_user(
            email="ops@kpmg.in",
            password=self.password,
            full_name="Ops",
            portal="ops",
        )

    def test_login_returns_tokens_with_claims(self):
        resp = self.client.post(
            reverse("accounts:login"),
            {"email": self.user.email, "password": self.password},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)
        access = AccessToken(resp.data["access"])
        self.assertEqual(access["portal"], "ops")
        self.assertEqual(access["email"], self.user.email)

    def test_login_with_bad_password_rejected(self):
        resp = self.client.post(
            reverse("accounts:login"),
            {"email": self.user.email, "password": "wrong"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class OTPFlowTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.candidate = User.objects.create_user(
            email="cand@example.com",
            full_name="Cand",
            portal="candidate",
            tenant_id=uuid.uuid4(),
        )
        Role.objects.create(name="candidate", portal="candidate", permissions=[])
        UserRole.objects.create(
            user=self.candidate,
            role=Role.objects.get(name="candidate"),
            tenant_id=self.candidate.tenant_id,
        )

    def test_otp_request_issues_code_and_returns_uniform_response(self):
        resp = self.client.post(
            reverse("accounts:otp-request"),
            {"email": self.candidate.email},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(OTPCode.objects.filter(user=self.candidate).count(), 1)

    def test_otp_request_for_unknown_email_returns_uniform_response(self):
        # Must not act as a user-enumeration oracle.
        resp = self.client.post(
            reverse("accounts:otp-request"),
            {"email": "ghost@example.com"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(OTPCode.objects.count(), 0)

    def test_otp_verify_returns_tokens(self):
        otp = OTPCode.generate_for_user(self.candidate)
        resp = self.client.post(
            reverse("accounts:otp-verify"),
            {"email": self.candidate.email, "code": otp.code},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        access = AccessToken(resp.data["access"])
        self.assertEqual(access["portal"], "candidate")
        self.assertEqual(access["tenant_id"], str(self.candidate.tenant_id))
        self.assertIn("candidate", access["roles"])

    def test_otp_verify_wrong_code_rejected(self):
        OTPCode.generate_for_user(self.candidate)
        resp = self.client.post(
            reverse("accounts:otp-verify"),
            {"email": self.candidate.email, "code": "000000"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class RefreshAndLogoutTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "changeme123"
        self.user = User.objects.create_user(
            email="logout@kpmg.in",
            password=self.password,
            full_name="LO",
            portal="ops",
        )
        resp = self.client.post(
            reverse("accounts:login"),
            {"email": self.user.email, "password": self.password},
            format="json",
        )
        self.access = resp.data["access"]
        self.refresh = resp.data["refresh"]

    def test_refresh_returns_new_access(self):
        resp = self.client.post(
            reverse("accounts:token-refresh"),
            {"refresh": self.refresh},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)

    def test_logout_blacklists_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        resp = self.client.post(
            reverse("accounts:logout"),
            {"refresh": self.refresh},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Using the blacklisted refresh must now fail.
        self.client.credentials()
        again = self.client.post(
            reverse("accounts:token-refresh"),
            {"refresh": self.refresh},
            format="json",
        )
        self.assertEqual(again.status_code, status.HTTP_401_UNAUTHORIZED)


class MeViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "changeme123"
        self.user = User.objects.create_user(
            email="me@kpmg.in",
            password=self.password,
            full_name="Me",
            portal="ops",
        )

    def test_me_requires_auth(self):
        resp = self.client.get(reverse("accounts:me"))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_user_payload_when_authenticated(self):
        login = self.client.post(
            reverse("accounts:login"),
            {"email": self.user.email, "password": self.password},
            format="json",
        )
        token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        resp = self.client.get(reverse("accounts:me"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["email"], self.user.email)
        self.assertEqual(resp.data["portal"], "ops")
