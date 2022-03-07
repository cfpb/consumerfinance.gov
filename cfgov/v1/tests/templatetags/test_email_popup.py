from unittest import TestCase

from django.conf import settings
from django.template import Context, Template
from django.test import RequestFactory, override_settings


class TestEmailPopupSettings(TestCase):
    def test_setting_should_be_dict(self):
        self.assertIsInstance(settings.EMAIL_POPUP_URLS, dict)

    def test_setting_keys_and_values(self):
        for k, v in settings.EMAIL_POPUP_URLS.items():
            self.assertIsInstance(k, str)
            self.assertIsInstance(v, list)


class TestEmailPopupTag(TestCase):
    def render(self, path):
        request = RequestFactory().get(path)
        template = Template("{% load email_popup %}{% email_popup request %}")
        return template.render(Context({"request": request}))

    @override_settings(EMAIL_POPUP_URLS={})
    def test_no_popups_configured_returns_blank(self):
        response = self.render("/no/pages/configured/")
        self.assertEqual(response, "")

    @override_settings(
        EMAIL_POPUP_URLS={"foo": ["/page/configured/"]}, FLAGS={}
    )
    def test_popup_configured_but_no_flag(self):
        response = self.render("/page/configured/")
        self.assertEqual(response, "")

    @override_settings(
        EMAIL_POPUP_URLS={"foo": ["/page/configured/"]},
        FLAGS={"EMAIL_POPUP_FOO": [("boolean", False)]},
    )
    def test_popup_configured_but_flag_false(self):
        response = self.render("/page/configured/")
        self.assertEqual(response, "")

    @override_settings(
        EMAIL_POPUP_URLS={"foo": ["/page/configured/"]},
        FLAGS={"EMAIL_POPUP_FOO": [("boolean", False)]},
    )
    def test_popup_configured_and_flag_true_but_path_doesnt_match(self):
        response = self.render("/page/not/configured/")
        self.assertEqual(response, "")

    @override_settings(
        EMAIL_POPUP_URLS={"oah": ["/page/configured/"]},
        FLAGS={"EMAIL_POPUP_OAH": [("boolean", True)]},
    )
    def test_popup_configured_and_flag_true_and_path_matches(self):
        response = self.render("/page/configured/")
        self.assertIn("o-email-popup_body", response)
