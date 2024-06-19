from django.test import TestCase, override_settings
from django.urls import reverse


class LoginViewTestCase(TestCase):
    @override_settings(ENABLE_SSO=True)
    def test_view_gets_sso_enabled_context(self):
        response = self.client.get(reverse("cfgov_login"))
        self.assertTrue(response.context["sso_enabled"])
        pass

    @override_settings(ENABLE_SSO=False)
    def test_view_gets_sso_disabled_context(self):
        response = self.client.get(reverse("cfgov_login"))
        self.assertFalse(response.context["sso_enabled"])
