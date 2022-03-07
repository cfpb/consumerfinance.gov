from django.test import Client, TestCase

from v1.models.landing_page import LandingPage
from v1.tests.wagtail_pages.helpers import publish_page, save_new_page


django_client = Client()


class PageStatesTestCase(TestCase):
    def test_draft_page(self):
        """Draft page should not load in www"""
        draft = LandingPage(
            title="Draft Page",
            slug="draft",
            live=False,
        )
        save_new_page(child=draft)
        www_response = django_client.get("/draft/")
        self.assertEqual(www_response.status_code, 404)

    def test_live_page(self):
        """Live page should load in www"""
        live_page = LandingPage(
            title="Live",
            slug="live",
            live=True,
        )
        publish_page(child=live_page)

        www_response = django_client.get("/live/")
        self.assertEqual(www_response.status_code, 200)

    def test_live_draft_page(self):
        """Live draft page should not display unpublished content"""
        live_draft = LandingPage(
            title="Page Before Updates",
            slug="page",
            live=False,
        )
        save_new_page(live_draft).publish()

        live_draft.title = "Draft Page Updates"
        live_draft.save_revision()

        www_response = django_client.get("/page/")

        self.assertNotContains(www_response, "Draft Page Updates")
        self.assertContains(www_response, "Page Before Updates")
