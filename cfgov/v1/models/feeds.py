from django.contrib.syndication.views import Feed
from wagtail.wagtailcore.url_routing import RouteResult

from datetime import datetime
import pytz

eastern = pytz.timezone('US/Eastern')


class FilterableFeed(Feed):
    item_guid_is_permalink = False

    def __init__(self, page, context):
        self.page = page
        self.context = context

    def link(self):
        return self.page.full_url

    def author_name(self):
        return "Consumer Financial Protection Bureau"

    def title(self):
        return "%s | Consumer Financial Protection Bureau" % self.page.title

    def items(self):
        return self.context['posts']

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

    def item_author_name(self, item):
        if hasattr(item, 'authors'):
            author_names = [a.name for a in item.authors.all()]
            author_string = ', '.join(author_names)
            return author_string

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
