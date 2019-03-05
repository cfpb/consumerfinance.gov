from v1.models.base import CFGOVPageManager
from v1.models.blog_page import BlogPage, LegacyBlogPage
from v1.atomic_elements.molecules import RSSFeed


class NewsroomPage(BlogPage):
    template = 'newsroom/newsroom-page.html'
    objects = CFGOVPageManager()

    def get_context(self, request):
        context = super(NewsroomPage, self).get_context(request)
        context['rss_url'] = RSSFeed.feed_urls['newsroom_feed']

        return context

class LegacyNewsroomPage(LegacyBlogPage):
    template = 'newsroom/newsroom-page.html'
    objects = CFGOVPageManager()
