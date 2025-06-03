from datetime import datetime, timezone

from django.contrib.sitemaps import Sitemap


class CFGOVSitemap(Sitemap):
    # Set a minimum lastmod date
    # This is to bring in changes that don't
    # propagate via publishing (metadata updates, etc)
    min_date = datetime(2025, 6, 4, 0, 0, 0, 0, tzinfo=timezone.utc)

    def __init__(self, request=None):
        self.request = request

    # Next two methods cribbed from https://github.com/wagtail/wagtail/blob/69e80629ac5996aeeca9d012c69f7095daa01422/wagtail/contrib/sitemaps/sitemap_generator.py#L21-L37
    def get_wagtail_site(self):
        from wagtail.models import Site

        site = Site.find_for_request(self.request)
        if site is None:
            return Site.objects.select_related("root_page").get(
                is_default_site=True
            )
        return site

    def items(self):
        return (
            self.get_wagtail_site()
            .root_page.get_descendants(inclusive=True)
            .live()
            .public()
            .order_by("path")
            .defer_streamfields()
            .specific()
        )

    def location(self, obj):
        return obj.get_url_parts()[2]

    def lastmod(self, obj):
        pub = obj.last_published_at
        if pub > self.min_date:
            return pub
        return self.min_date
