from unittest import TestCase

from core.templatetags.signed_redirect import is_url


class TestIsUrl(TestCase):
    def test_null(self):
        self.assertFalse(is_url(None))

    def test_blank(self):
        self.assertFalse(is_url(""))

    def test_http(self):
        self.assertTrue(is_url("http://www.foo.com"))

    def test_https(self):
        self.assertTrue(is_url("https://www.foo.com"))

    def test_no_http(self):
        self.assertTrue(is_url("www.foo.com"))
