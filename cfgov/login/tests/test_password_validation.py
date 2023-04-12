from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.test import TestCase

from freezegun import freeze_time

from login.models import PasswordHistoryItem
from login.password_validation import (
    AgeValidator,
    ComplexityValidator,
    HistoryValidator,
)


User = get_user_model()


class TestComplexityValidator(TestCase):
    def test_complexity_validation_error(self):
        validator = ComplexityValidator(
            rules=[
                (r"[A-Z]", "Password require a capital letter"),
            ],
        )
        with self.assertRaises(ValidationError):
            validator.validate("testing")

    def test_complexity_validation_with_configured_rules(self):
        rules = next(
            validator_conf["OPTIONS"]["rules"]
            for validator_conf in settings.AUTH_PASSWORD_VALIDATORS
            if validator_conf["NAME"]
            == "login.password_validation.ComplexityValidator"
        )
        validator = ComplexityValidator(rules=rules)

        with self.assertRaises(ValidationError) as cm:
            validator.validate("test")
        self.assertEqual(
            cm.exception.message,
            "Password must include at least one capital letter",
        )

        with self.assertRaises(ValidationError) as cm:
            validator.validate("TEST")
        self.assertEqual(
            cm.exception.message,
            "Password must include at least one lowercase letter",
        )

        with self.assertRaises(ValidationError) as cm:
            validator.validate("Test")
        self.assertEqual(
            cm.exception.message, "Password must include at least one digit"
        )

        with self.assertRaises(ValidationError) as cm:
            validator.validate("Test1")
        self.assertEqual(
            cm.exception.message,
            "Password must include at least one special character (@#$%&!)",
        )


class ValidatorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test_user", email="test@example.com"
        )

    def test_age_validation_new_user(self):
        # New users can always reset their password.
        AgeValidator(hours=1).validate("testing", user=self.user)

    def test_age_validation(self):
        with freeze_time("9999-01-01") as frozen_time:
            PasswordHistoryItem.objects.create(
                user=self.user,
                encrypted_password=make_password("testing"),
            )

            # Fast forward time by 90 minutes.
            frozen_time.tick(60 * 90)

            # AgeValidator with a 1 hour check will pass validation,
            # because password was last set over an hour ago.
            AgeValidator(hours=1).validate("testing", user=self.user)

            # AgeValidator with a 2 hour check will fail validation,
            # because password was last set less than 2 hours ago.
            with self.assertRaises(ValidationError) as e:
                AgeValidator(hours=2).validate("testing", user=self.user)

            self.assertIn("once in 2 hours", e.exception.message)

    def test_age_validation_superuser(self):
        PasswordHistoryItem.objects.create(
            user=self.user, encrypted_password=make_password("testing")
        )

        self.user.is_superuser = True

        # AgeValidator with a 1 hour check will pass validation,
        # even though password was last set less than an hour ago,
        # because the user is a superuser.
        AgeValidator(hours=1).validate("testing", user=self.user)

    def test_history_validation(self):
        # Make a history of 10 passwords, "testing0" ... "testing9".
        for i in range(10):
            PasswordHistoryItem.objects.create(
                user=self.user, encrypted_password=make_password(f"testing{i}")
            )

        # A validator that checks the last 5 passwords will pass "testing0".
        HistoryValidator(count=5).validate("testing0", user=self.user)

        # A validator that checks the last 10 passwords will fail "testing0".
        with self.assertRaises(ValidationError) as e:
            HistoryValidator(count=10).validate("testing0", user=self.user)

        self.assertIn("last 10 passwords", e.exception.message)
