from datetime import datetime, timezone

from django.test import RequestFactory, TestCase

from cfgov.sitemap import CFGOVSitemap


class CFGOVSitemapTestCase(TestCase):
    def make_sitemap(self):
        request = RequestFactory().get("/sitemap.xml")
        return CFGOVSitemap(request)

    def test_site(self):
        sitemap = self.make_sitemap()
        site = sitemap.get_wagtail_site()
        self.assertIsNotNone(site)

    def test_items(self):
        sitemap = self.make_sitemap()
        self.assertGreater(len(sitemap.items()), 0)

    def test_location(self):
        sitemap = self.make_sitemap()
        page = sitemap.items()[0]
        self.assertEqual(sitemap.location(page), "/")

    def test_lastmod(self):
        sitemap = self.make_sitemap()
        page = sitemap.items()[0]
        page.last_published_at = datetime(
            2025, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc
        )
        self.assertEqual(sitemap.min_date, sitemap.lastmod(page))

        page.last_published_at = datetime(
            2026, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc
        )
        self.assertEqual(page.last_published_at, sitemap.lastmod(page))
