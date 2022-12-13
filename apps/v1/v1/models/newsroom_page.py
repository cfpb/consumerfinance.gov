from v1.models.blog_page import BlogPage, LegacyBlogPage


class NewsroomPage(BlogPage):
    template = "v1/newsroom/newsroom-page.html"


class LegacyNewsroomPage(LegacyBlogPage):
    template = "v1/newsroom/newsroom-page.html"
