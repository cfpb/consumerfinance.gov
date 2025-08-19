from datetime import datetime

from django.shortcuts import reverse

from core.testutils.test_cases import WagtailPageTreeTestCase
from v1.models import LearnPage


class SitemapTests(WagtailPageTreeTestCase):
    @classmethod
    def get_page_tree(cls):
        return [
            (
                LearnPage(
                    title="old",
                    live=True,
                    last_published_at=datetime(1970, 1, 1),
                )
            )
        ]

    def test_sitemap(self):
        response = self.client.get(reverse("sitemap"))

        # Pages with dates older than Sitemap.MIN_SITEMAP_DATE are given newer
        # dates in the sitemap.
        self.assertEqual(
            response.content,
            (
                b'<?xml version="1.0" encoding="UTF-8"?>\n'
                b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                b"<url><loc>http://localhost/</loc><lastmod>2025-07-08</lastmod></url>"
                b"<url><loc>http://localhost/old/</loc><lastmod>2025-07-08</lastmod></url>\n"
                b"</urlset>\n"
            ),
        )

        # The Last-Modified header should also be set appropriately.
        self.assertEqual(
            response["Last-Modified"], "Wed, 09 Jul 2025 00:00:00 GMT"
        )
