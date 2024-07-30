import re

from django.test import SimpleTestCase

from tccp.jinja2tags import (
    _format_contact_phone_number,
    _format_contact_website,
    render_contact_info,
)


class FormatContactPhoneNumberTests(SimpleTestCase):
    def test_phone_number_formatting(self):
        for value, expected in [
            ("FOOBAR", "FOOBAR"),
            ("888-FOO-BAR", "888FOOBAR"),
            ("18885551234", "8885551234"),
            ("(800) 555-1234", "8005551234"),
        ]:
            with self.subTest(value=value, expected=expected):
                self.assertEqual(_format_contact_phone_number(value), expected)


class FormatContactWebsiteTests(SimpleTestCase):
    def test_website_formatting(self):
        for value, expected in [
            (
                "http://example.com",
                {"text": "example.com", "url": "http://example.com"},
            ),
            (
                "https://example.com",
                {"text": "example.com", "url": "https://example.com"},
            ),
            (
                "https://www.example.com",
                {
                    "text": "example.com",
                    "url": "https://www.example.com",
                },
            ),
            (
                "https://subdomain.example.com",
                {
                    "text": "subdomain.example.com",
                    "url": "https://subdomain.example.com",
                },
            ),
            (
                "https://example.com/path/",
                {
                    "text": "example.com",
                    "url": "https://example.com/path/",
                },
            ),
            (
                "invalid://example.com",
                {
                    "text": "invalid://example.com",
                },
            ),
            (
                "example.com",
                {
                    "text": "example.com",
                },
            ),
        ]:
            with self.subTest(value=value, expected=expected):
                self.assertEqual(_format_contact_website(value), expected)


class TestRenderContactInfo(SimpleTestCase):
    def test_render(self):
        html = render_contact_info(
            {
                "website_for_consumer": "https://example.com foo.com",
                "telephone_number_for_consumers": "1 212-555-1234",
            }
        )

        self.assertEqual(len(re.findall("m-contact-hyperlink", html)), 2)
        self.assertIn('<a href="https://example.com">', html)
        self.assertNotIn('<a href="foo.com">', html)
        self.assertEqual(len(re.findall("m-contact-phone", html)), 1)
        self.assertIn("2125551234", html)
