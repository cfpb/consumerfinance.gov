from django.conf import settings
from django.test import SimpleTestCase, override_settings

from core.feature_flags import environment_is, environment_is_not


class TestEnvironmentConditions(SimpleTestCase):
    @override_settings()
    def test_setting_not_defined(self):
        del settings.DEPLOY_ENVIRONMENT
        self.assertFalse(environment_is("foo"))
        self.assertTrue(environment_is_not("foo"))

    @override_settings(DEPLOY_ENVIRONMENT="foo")
    def test_setting_matches(self):
        self.assertTrue(environment_is("foo"))
        self.assertFalse(environment_is_not("foo"))

    @override_settings(DEPLOY_ENVIRONMENT="bar")
    def test_setting_does_not_match(self):
        self.assertFalse(environment_is("foo"))
        self.assertTrue(environment_is_not("foo"))
