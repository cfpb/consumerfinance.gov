import json

from django.test import TestCase

from v1.models.blog_page import BlogPage
from v1.models.browse_page import BrowsePage
from v1.models.snippets import Contact
from v1.tests.wagtail_pages.helpers import publish_page


class ExternalLinksSearchViewTestCase(TestCase):

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_get(self):
        response = self.client.get("/admin/external-links/")
        self.assertEqual(response.status_code, 200)

    def test_empty_url(self):
        response = self.client.post("/admin/external-links/", {"url": ""})
        self.assertEqual(response.status_code, 200)

    def test_no_results(self):
        response = self.client.post(
            "/admin/external-links/", {"url": "www.foobar.com"}
        )
        self.assertContains(
            response, "There are no matching pages or snippets"
        )

    def test_snippet_results(self):
        contact = Contact(body="<a href=https://www.foobar.com>...</a>")
        contact.save()
        response = self.client.post(
            "/admin/external-links/", {"url": "www.foobar.com"}
        )
        self.assertContains(
            response, "There are 0 matching pages and 1 matching snippet"
        )

    def test_page_results(self):
        page = BrowsePage(
            title="Test Browse Page",
            slug="test-browse-page",
            content=json.dumps(
                [
                    {
                        "type": "well",
                        "value": {
                            "content": "<a href=https://www.foobar.com>...</a>"
                        },
                    }
                ]
            ),
        )
        publish_page(page)

        response = self.client.post(
            "/admin/external-links/", {"url": "www.foobar.com"}
        )
        self.assertContains(
            response,
            "There is 1 matching page and 0 matching snippets"
        )

    def test_single_result_per_page(self):
        """ Page should show up once in results,
        even if the same link occurs multiple times in it.
        """
        page = BlogPage(
            title="Test Blog Page",
            slug="test-blog-page",
            content=json.dumps(
                [
                    {
                        "type": "well",
                        "value": {
                            "content": "<a href=https://www.foobar.com>...</a>"
                        },
                    }
                ]
            ),
            header=json.dumps(
                [
                    {
                        "type": "text_introduction",
                        "value": {
                            "intro": "<a href=https://www.foobar.com>...</a>"
                        },
                    }
                ]
            ),
        )
        publish_page(page)

        response = self.client.post(
            "/admin/external-links/", {"url": "www.foobar.com"}
        )
        self.assertContains(
            response,
            "There is 1 matching page and 0 matching snippets"
        )

    def test_no_duplicates(self):
        """ Page should show up once in results,
        even if field the link is in belongs to a parent page
        """
        page = BlogPage(
            title="Test Blog Page",
            slug="test-blog-page",
            sidefoot=json.dumps(
                [
                    {
                        "type": "related_links",
                        "value": {
                            "links": [
                                {"url": "https://www.foobar.com", "text": ""}
                            ]
                        },
                    }
                ]
            ),
        )
        publish_page(page)
        response = self.client.post(
            "/admin/external-links/", {"url": "www.foobar.com"}
        )
        self.assertContains(
            response, "There is 1 matching page and 0 matching snippets"
        )
