from django.apps import apps
from django.core.checks import Info
from django.test import TestCase, override_settings

from login.checks import check_oidc_admin_role_setting


class ChecksTestCase(TestCase):
    @override_settings(ENABLE_SSO=True, OIDC_OP_ADMIN_ROLE=None)
    def test_check_oidc_admin_role_setting(self):
        errors = check_oidc_admin_role_setting(apps.get_app_configs())
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], Info)
        self.assertEqual(errors[0].id, "login.I001")
