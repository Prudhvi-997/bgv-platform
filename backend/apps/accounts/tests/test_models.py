"""Unit tests for the User and Role models."""
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.accounts.models import Role


User = get_user_model()


class UserModelTests(TestCase):
    def test_create_candidate_user_no_password(self):
        user = User.objects.create_user(
            email="cand@example.com",
            full_name="Cand Idate",
            portal="candidate",
        )
        self.assertEqual(user.email, "cand@example.com")
        self.assertEqual(user.portal, "candidate")
        self.assertFalse(user.has_usable_password())
        self.assertIsNone(user.tenant_id)

    def test_create_ops_user_with_password(self):
        user = User.objects.create_user(
            email="ops@kpmg.in",
            password="changeme123",
            full_name="Ops One",
            portal="ops",
        )
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.check_password("changeme123"))

    def test_email_is_unique(self):
        User.objects.create_user(
            email="dup@example.com", full_name="A", portal="ops",
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="dup@example.com", full_name="B", portal="client",
            )

    def test_email_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="", full_name="X", portal="ops",
            )

    def test_str_repr_contains_email_and_portal(self):
        user = User.objects.create_user(
            email="repr@example.com", full_name="R", portal="ops",
        )
        self.assertIn("repr@example.com", str(user))
        self.assertIn("ops", str(user))


class RoleModelTests(TestCase):
    def test_role_uniqueness_per_portal(self):
        Role.objects.create(name="dup", portal="ops", permissions=["a"])
        with self.assertRaises(IntegrityError):
            Role.objects.create(name="dup", portal="ops", permissions=["b"])

    def test_same_role_name_different_portal_allowed(self):
        Role.objects.create(name="reviewer", portal="ops", permissions=[])
        Role.objects.create(name="reviewer", portal="vendor", permissions=[])
        self.assertEqual(Role.objects.filter(name="reviewer").count(), 2)
