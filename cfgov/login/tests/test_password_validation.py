from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from login.password_validation import PasswordRegexValidator


User = get_user_model()


class ValidatorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test_user", email="test@example.com"
        )

    def test_regex_validation_error(self):
        validator = PasswordRegexValidator(
            regex=r"[A-Z]",
            message="Password require a capital letter",
        )
        with self.assertRaises(ValidationError):
            validator.validate("testing")
