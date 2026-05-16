"""Unit tests for OTP generation, expiry, and single-use semantics."""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import OTP_LIFETIME, OTPCode


User = get_user_model()


class OTPTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="cand@example.com",
            full_name="Cand",
            portal="candidate",
        )

    def test_generate_otp_creates_six_digit_code_with_ten_minute_expiry(self):
        otp = OTPCode.generate_for_user(self.user)
        self.assertEqual(len(otp.code), 6)
        self.assertTrue(otp.code.isdigit())
        self.assertFalse(otp.is_used)
        # Window of a couple of seconds for clock drift in the assertion.
        expected = timezone.now() + OTP_LIFETIME
        self.assertLess(abs((otp.expires_at - expected).total_seconds()), 5)

    def test_verify_otp_succeeds_once_then_fails(self):
        otp = OTPCode.generate_for_user(self.user)
        self.assertTrue(OTPCode.verify_for_user(self.user, otp.code))
        # Reusing the same code must fail.
        self.assertFalse(OTPCode.verify_for_user(self.user, otp.code))
        otp.refresh_from_db()
        self.assertTrue(otp.is_used)

    def test_verify_wrong_code_fails(self):
        OTPCode.generate_for_user(self.user)
        self.assertFalse(OTPCode.verify_for_user(self.user, "000000"))

    def test_expired_otp_rejected(self):
        otp = OTPCode.generate_for_user(self.user)
        # Force expiry by rewinding the row.
        OTPCode.objects.filter(pk=otp.pk).update(
            expires_at=timezone.now() - timedelta(seconds=1)
        )
        self.assertFalse(OTPCode.verify_for_user(self.user, otp.code))

    def test_new_otp_request_invalidates_prior_unused_otps(self):
        first = OTPCode.generate_for_user(self.user)
        second = OTPCode.generate_for_user(self.user)
        first.refresh_from_db()
        self.assertTrue(first.is_used)  # invalidated by issuance of `second`
        self.assertFalse(second.is_used)
        # The first code must no longer verify.
        self.assertFalse(OTPCode.verify_for_user(self.user, first.code))
        # The second code must verify exactly once.
        self.assertTrue(OTPCode.verify_for_user(self.user, second.code))

    def test_is_expired_helper(self):
        otp = OTPCode.generate_for_user(self.user)
        self.assertFalse(otp.is_expired())
        OTPCode.objects.filter(pk=otp.pk).update(
            expires_at=timezone.now() - timedelta(seconds=1)
        )
        otp.refresh_from_db()
        self.assertTrue(otp.is_expired())
