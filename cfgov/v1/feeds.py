from datetime import datetime

from django.contrib.syndication.views import Feed


try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from django.utils.timezone import make_aware


eastern = zoneinfo.ZoneInfo("US/Eastern")


class FilterableFeed(Feed):
    item_guid_is_permalink = False

    def __init__(self, request, page, items):
        self.request = request
        self.page = page
        self.items = items

    def link(self):
        return self.page.get_full_url(self.request)

    def title(self):
        return f"{self.page.title} | Consumer Financial Protection Bureau"

    def item_link(self, item):
        return item["full_url"]

    def item_pubdate(self, item):
        item_date = item["date_published"]
        naive = datetime.combine(item_date, datetime.min.time())
        return make_aware(naive, eastern)

    def item_title(self, item):
        return item["title"]

    def item_description(self, item):
        return item["search_description"]

    def item_categories(self, item):
        return [category["name"] for category in item["categories"]] + [
            tag["text"] for tag in item["tags"]
        ]

    def item_guid(self, item):
        return f"{item['page_id']}<>consumerfinance.gov"


def get_appropriate_rss_feed_url_for_page(page, request=None):
    """Given a page, return the most appropriate RSS feed for it to link to.

    This may be the page itself if the specified page provides a feed (for
    example if the specified page is a blog index page) or may be the
    specified page's closest ancestor that provides a feed (for example if the
    specified page is an individual blog page that lives in the tree somewhere
    under the index page).

    Pages are considered to provide a feed if they inherit from
    AbstractFilterablePage.

    Returns None if neither the page nor any of its ancestors provide feeds.
    """
    from v1.models.filterable_page import AbstractFilterablePage

    ancestors_including_page = page.get_ancestors(inclusive=True)
    ancestors_including_page_with_feeds = ancestors_including_page.filter(
        ancestors_including_page.type_q(AbstractFilterablePage)
    )

    # page.get_ancestors() orders from root down to page.
    rss_feed_providing_page = ancestors_including_page_with_feeds.last()

    if rss_feed_providing_page:
        page_url = rss_feed_providing_page.get_url(request=request)
        return page_url + "feed/"
