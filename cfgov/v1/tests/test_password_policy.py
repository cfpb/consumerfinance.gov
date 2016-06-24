import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from mock import patch

from ..util import password_policy

PASSWORD_RULES = [
    [r'.{12,}', 'Minimum allowed length is 12 characters'],
    [r'[A-Z]', 'must include at least one capital letter'],
    [r'[a-z]', 'must include at least one lowercase letter'],
    [r'[0-9]', 'must include at least one digit'],
    [r'[@#$%&!]', 'must include at least one special character (@#$%&!)'],
]

POLICY_SETTING = 'django.conf.settings.CFPB_COMMON_PASSWORD_RULES'


class TestPasswordValidation(TestCase):

    @patch(POLICY_SETTING, PASSWORD_RULES)
    def test_bad_passwords(self):
        for password in ['T00Short!', 'no_c@pital_l3tters',
                         'NO_LOWERCASE_L3TTERS!', '#Everything_but_digits!',
                         'No8Special7Characters8675309', 'Tr0ub4dor&3',
                         'correct_horse_battery_staple']:
            with self.assertRaises(ValidationError):
                    password_policy.validate_password_all_rules(password, 'key')

    def test_good_passwords(self):
        for password in ['1976IndyD3claration!', 'XkCd936HasAGoodPoint!']:
            # confession: I spent a good few minutes looking for something like
            # assertDoesNotRaise.
            password_policy.validate_password_all_rules(password, 'key')


class TestWithUser(TestCase):
    def setUp(self):
        user = User(username='testuser', password=make_password('password')) 
        user.save()

    def tearDown(self):
        User.objects.get(username='testuser').delete()

    def get_user(self):
        return User.objects.get(username='testuser')


class TestMinimumPasswordAge(TestWithUser):

    def test_too_soon(self):
        user = self.get_user()
        history_item = user.passwordhistoryitem_set.latest()
        current_locked_until = history_item.locked_until
        new_locked_until = current_locked_until.replace(year=datetime.MAXYEAR)
        history_item.locked_until = new_locked_until
        history_item.save()
        with self.assertRaises(ValidationError):
            password_policy.validate_password_age(user)

    def test_old_enough_to_change(self):
        user = self.get_user()
        history_item = user.passwordhistoryitem_set.get()

        current_lock_expires = history_item.locked_until
        new_expiration = current_lock_expires.replace(year=2013)
        history_item.locked_until = new_expiration
        history_item.save()

        password_policy.validate_password_age(user)


class TestPasswordReusePolicy(TestWithUser):
    def test_reuse_password(self):
        user = self.get_user()
        with self.assertRaises(ValidationError):
            password_policy.validate_password_history(user, 'password')

    def test_new_password(self):
        user = self.get_user()
        password_policy.validate_password_history(user, 'new_password')
