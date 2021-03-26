from django.test import TestCase

from v1.models.banners import Banner


class TestBanner(TestCase):
    def test_banner_str_method(self):
        test_banner = Banner(title="Test banner")
        self.assertEqual(str(test_banner), test_banner.title)
