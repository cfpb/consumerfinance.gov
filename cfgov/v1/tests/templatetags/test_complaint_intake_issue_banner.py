from unittest import TestCase

from django.conf import settings
from django.template import Context, Template
from django.test import RequestFactory, SimpleTestCase, override_settings


class TestComplaintBannerSettings(TestCase):
    def test_setting_should_be_list(self):
        self.assertIsInstance(settings.COMPLAINT_INTAKE_TECHNICAL_ISSUES_URLS, list)

    def test_setting_values(self):
        for url in settings.COMPLAINT_INTAKE_TECHNICAL_ISSUES_URLS:
            self.assertIsInstance(url, str)

class TestComplaintBannerTag(TestCase):
    def render(self, path):
        request = RequestFactory().get(path)
        template = Template('{% load complaint_issue_banner %}{% complaint_issue_banner request %}')
        return template.render(Context({'request': request}))

    @override_settings(COMPLAINT_INTAKE_TECHNICAL_ISSUES_URLS=[])
    def test_no_urls_configured_returns_blank(self):
        response = self.render('/no/pages/configured/')
        self.assertEqual(response, '')

    @override_settings(
        COMPLAINT_INTAKE_TECHNICAL_ISSUES_URLS=['/page/configured/']
    )
    def test_url_configuredand_path_matches(self):
        response = self.render('/page/configured/')
        self.assertIn('m-global-banner', response)
