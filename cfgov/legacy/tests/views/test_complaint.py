from django.test import TestCase, override_settings
from django.urls import reverse


class ComplaintLandingViewTests(TestCase):

    def setUp(self):
        self.search_url = reverse("complaint-search")

    def test_search_page_cache_tag(self):
        response = self.client.get(self.search_url)
        self.assertTrue(response.has_header("Edge-Cache-Tag"))
