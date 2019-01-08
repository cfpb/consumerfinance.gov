from django.test import TestCase, override_settings

import mock

from core.conditional_urls import include_if_app_enabled


class ConditionalURLTests(TestCase):

    @override_settings(
        INSTALLED_APPS=['core'],
    )
    @mock.patch('core.conditional_urls.include')
    def test_include_if_app_enabled_calls_include(self, mock_include):
        """ Test that an app gets include()ed when all conditions are met """
        include_if_app_enabled('core', None)
        self.assertEqual(mock_include.call_count, 1)

    @override_settings(
        INSTALLED_APPS=[],
    )
    @mock.patch('core.conditional_urls.wagtail_fail_through')
    def test_include_if_app_enabled_not_in_installed_apps(
            self, mock_wagtail_fail_through):
        """ Test that fail-through is called if app isn't in INSTALLED_APPS
        """
        result = include_if_app_enabled('core', None)
        self.assertEqual(mock_wagtail_fail_through, result)
