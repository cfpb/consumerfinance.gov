from django.test import TestCase
from django.core.exceptions import ValidationError

from mock import patch

from .util import password_policy

PASSWORD_RULES = [
    [r'.{12,}', 'Minimum allowed length is 12 characters'],
    [r'[A-Z]', 'must include at least one capital letter'],
    [r'[a-z]', 'must include at least one lowercase letter'],
    [r'[0-9]', 'must include at least one digit'],
    [r'[@#$%&!]', 'must include at least one special character (@#$%&!)'],
]

POLICY_SETTING = 'django.conf.settings.CFPB_COMMON_PASSWORD_RULES'


class TestPasswordPolicy(TestCase):

    @patch(POLICY_SETTING, PASSWORD_RULES)
    def test_rules_engine(self):
        with self.assertRaises(ValidationError):
                password_policy.validate_password_all_rules('invalid')

