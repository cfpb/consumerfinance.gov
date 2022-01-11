from django.test import TestCase, override_settings
from django.urls import reverse


class ComplaintLandingViewTests(TestCase):

    def setUp(self):
        self.landing_url = reverse("complaint-landing")
        self.search_url = reverse("complaint-search")

    @override_settings(
        FLAGS={"CCDB_TECHNICAL_ISSUES": [("boolean", False)]})
    def test_no_banner_when_flag_disabled(self):
        response = self.client.get(self.landing_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "m-notification_explanation")

    @override_settings(
        FLAGS={"CCDB_TECHNICAL_ISSUES": [("boolean", True)]})
    def test_banner_when_flag_enabled(self):
        response = self.client.get(self.landing_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "m-notification_explanation")

    def test_landing_page_cache_tag(self):
        response = self.client.get(self.landing_url)
        self.assertTrue(response.has_header("Edge-Cache-Tag"))

    def test_search_page_cache_tag(self):
        response = self.client.get(self.search_url)
        self.assertTrue(response.has_header("Edge-Cache-Tag"))
