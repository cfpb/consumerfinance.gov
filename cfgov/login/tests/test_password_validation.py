from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from login.models import PasswordHistoryItem
from login.password_validation import (
    AgeValidator,
    ComplexityValidator,
    HistoryValidator,
)


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


class TestAgeValidator(TestCase):
    def test_age_validation_error(self):
        UserModel = get_user_model()
        user = UserModel.objects.create_user(
            "test_user", email="test@example.com"
        )
        last_password = make_password("testing")
        PasswordHistoryItem(
            user=user,
            encrypted_password=last_password,
            locked_until=timezone.now() + timedelta(hours=1),
            expires_at=timezone.now() + timedelta(days=90),
        ).save()

        validator = AgeValidator()
        with self.assertRaises(ValidationError):
            validator.validate("testing", user=user)


class TestHistoryValidator(TestCase):
    def test_history_validation_error(self):
        UserModel = get_user_model()
        user = UserModel.objects.create_user(
            "test_user", email="test@example.com"
        )
        last_password = make_password("testing")
        PasswordHistoryItem(
            user=user,
            encrypted_password=last_password,
            locked_until=timezone.now() + timedelta(hours=1),
            expires_at=timezone.now() + timedelta(days=90),
        ).save()

        validator = HistoryValidator()
        with self.assertRaises(ValidationError):
            validator.validate("testing", user=user)
