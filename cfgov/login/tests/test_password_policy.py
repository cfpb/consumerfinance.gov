from datetime import timedelta
from unittest.mock import Mock, patch

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

import login.utils as password_policy

from v1.models import PasswordHistoryItem


PASSWORD_RULES = [
    [r".{12,}", "Minimum allowed length is 12 characters"],
    [r"[A-Z]", "must include at least one capital letter"],
    [r"[a-z]", "must include at least one lowercase letter"],
    [r"[0-9]", "must include at least one digit"],
    [r"[@#$%&!]", "must include at least one special character (@#$%&!)"],
]

POLICY_SETTING = "django.conf.settings.CFPB_COMMON_PASSWORD_RULES"


class TestPasswordValidation(TestCase):
    @patch(POLICY_SETTING, PASSWORD_RULES)
    def test_bad_passwords(self):
        for password in [
            "T00Short!",
            "no_c@pital_l3tters",
            "NO_LOWERCASE_L3TTERS!",
            "#Everything_but_digits!",
            "No8Special7Characters8675309",
            "Tr0ub4dor&3",
            "correct_horse_battery_staple",
        ]:
            with self.assertRaises(ValidationError):
                password_policy.validate_password_all_rules(password, "key")

    def test_good_passwords(self):
        for password in ["1976IndyD3claration!", "XkCd936HasAGoodPoint!"]:
            # confession: I spent a good few minutes looking for something like
            # assertDoesNotRaise.
            password_policy.validate_password_all_rules(password, "key")


class TestWithUser(TestCase):
    def get_user(self, last_password="password", pw_locked_until=None):
        encrypted_password = make_password(last_password)

        if not pw_locked_until:
            pw_locked_until = timezone.now()

        last_password_change = PasswordHistoryItem(
            encrypted_password=encrypted_password, locked_until=pw_locked_until
        )

        password_history = Mock(spec=PasswordHistoryItem.objects)
        password_history.latest.return_value = last_password_change
        password_history.order_by.return_value = [last_password_change]

        return Mock(
            username="testuser",
            password=encrypted_password,
            passwordhistoryitem_set=password_history,
        )


class TestMinimumPasswordAge(TestWithUser):
    def test_can_set_password_if_unlocked(self):
        yesterday = timezone.now() - timedelta(days=1)
        user = self.get_user(pw_locked_until=yesterday)
        password_policy.validate_password_age(user)

    def test_cant_set_password_if_locked(self):
        tomorrow = timezone.now() + timedelta(days=1)
        user = self.get_user(pw_locked_until=tomorrow)
        self.assertRaises(
            ValidationError, password_policy.validate_password_age, user
        )


class TestPasswordReusePolicy(TestWithUser):
    def test_can_set_new_password(self):
        user = self.get_user(last_password="password1")
        password_policy.validate_password_history(user, "password2")

    def test_cant_reuse_password(self):
        password = "password"
        user = self.get_user(last_password=password)
        self.assertRaises(
            ValidationError,
            password_policy.validate_password_history,
            user,
            password,
        )
