from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from .models import LegacyBlogPage

class BlogFeed(Feed):
    title = "CFPB Blog RSS Feed"
    link = "/feed/blog/"
    description = "The official blog of the Consumer Financial Protection Bureau"

    def items(self):
        return LegacyBlogPage.objects.live().order_by('-date_published')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.preview_description

    # item_link is only needed if LegacyBlogPage has no get_absolute_url method.
    def item_link(self, item):
        return item.url
