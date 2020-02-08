from datetime import datetime

from django.contrib.syndication.views import Feed

import pytz


try:
    from wagtail.core.url_routing import RouteResult
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore.url_routing import RouteResult


eastern = pytz.timezone('US/Eastern')


class FilterableFeed(Feed):
    item_guid_is_permalink = False

    def __init__(self, page, context):
        self.page = page
        self.context = context

    def link(self):
        return self.page.full_url

    def title(self):
        return "%s | Consumer Financial Protection Bureau" % self.page.title

    def items(self):
        posts = self.context['filter_data']['page_set']
        return posts

    def item_link(self, item):
        return item.full_url

    def item_pubdate(self, item):
        # this seems to require a datetime
        item_date = item.date_published
        naive = datetime.combine(item_date, datetime.min.time())
        return eastern.localize(naive)

    def item_description(self, item):
        return item.preview_description

    def item_categories(self, item):
        categories = [cat.get_name_display() for cat in item.categories.all()]
        tags = [tag.name for tag in item.tags.all()]
        return categories + tags

    def item_guid(self, item):
        return "%s<>consumerfinance.gov" % item.page_ptr_id


class FilterableFeedPageMixin(object):

    def route(self, request, path_components):
        if len(path_components) == 1 and path_components[0] == 'feed':
            return RouteResult(self, kwargs={'format': 'rss'})

        return super(FilterableFeedPageMixin,
                     self).route(request, path_components)

    def serve(self, request, format='html'):
        if format == 'rss':
            context = self.get_context(request)
            return FilterableFeed(self, context)(request)
        else:
            return super(FilterableFeedPageMixin, self).serve(request)


def get_appropriate_rss_feed_url_for_page(page, request=None):
    """Given a page, return the most appropriate RSS feed for it to link to.

    This may be the page itself if the specified page provides a feed (for
    example if the specified page is a blog index page) or may be the
    specified page's closest ancestor that provides a feed (for example if the
    specified page is an individual blog page that lives in the tree somewhere
    under the index page).

    Pages are considered to provide a feed if they inherit from
    FilterableFeedPageMixin.

    Returns None if neither the page nor any of its ancestors provide feeds.
    """
    ancestors_including_page = page.get_ancestors(inclusive=True)
    ancestors_including_page_with_feeds = ancestors_including_page.filter(
        ancestors_including_page.type_q(FilterableFeedPageMixin)
    )

    # page.get_ancestors() orders from root down to page.
    rss_feed_providing_page = ancestors_including_page_with_feeds.last()

    if rss_feed_providing_page:
        page_url = rss_feed_providing_page.get_url(request=request)
        return page_url + 'feed/'
