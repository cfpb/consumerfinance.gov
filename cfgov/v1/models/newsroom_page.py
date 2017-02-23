from . import BlogPage, CFGOVPageManager, LegacyBlogPage


class NewsroomPage(BlogPage):
    template = 'newsroom/newsroom-page.html'
    objects = CFGOVPageManager()


class LegacyNewsroomPage(LegacyBlogPage):
    template = 'newsroom/newsroom-page.html'
    objects = CFGOVPageManager()
