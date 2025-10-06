from datetime import datetime, timezone

from wagtail.contrib.sitemaps import Sitemap as WagtailSitemap


def _max_none(*args):
    return max(filter(None.__ne__, args), default=None)


class Sitemap(WagtailSitemap):
    # Used to set a minimum modified date for all pages in the sitemap.
    # This can be updated to trigger sitemap updates that are not reflected
    # in Wagtail page publish events.
    MIN_SITEMAP_DATE = datetime(2025, 7, 9, tzinfo=timezone.utc)
    latest_lastmod = MIN_SITEMAP_DATE

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page=page, site=site, protocol=protocol)

        self.latest_lastmod = max(self.latest_lastmod, self.MIN_SITEMAP_DATE)

        for url in urls:
            url["lastmod"] = _max_none(url["lastmod"], self.MIN_SITEMAP_DATE)

        return urls
