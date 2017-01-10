from . import BlogPage, LegacyBlogPage


class NewsroomPage(BlogPage):
    template = 'newsroom/newsroom-page.html'


class LegacyNewsroomPage(LegacyBlogPage):
    template = 'newsroom/newsroom-page.html'
