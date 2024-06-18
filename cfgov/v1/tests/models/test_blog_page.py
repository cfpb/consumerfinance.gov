from django.test import RequestFactory, TestCase

from v1.models import BlogPage, SublandingFilterablePage
from v1.tests.wagtail_pages.helpers import save_new_page


class BlogPageTests(TestCase):
    def test_unpublished_page_doesnt_include_rss_feed(self):
        page = BlogPage(title="test", slug="test")

        request = RequestFactory().get("/")
        response = page.serve(request)

        self.assertNotContains(response, "RSS feed")

    def test_page_includes_rss_feed_of_parent(self):
        parent_page = SublandingFilterablePage(title="test", slug="test")
        save_new_page(parent_page)

        child_page = BlogPage(title="test", slug="test")
        save_new_page(child_page, root=parent_page)

        response = self.client.get("/test/test/")
        self.assertContains(response, 'href="/test/feed/')

    def test_preview_modes(self):
        page = BlogPage(title="test")
        self.assertIn("list_view", dict(page.preview_modes))

    def render_preview(self, mode_name=None):
        page = BlogPage(title="test")
        request = RequestFactory().get("/")
        return page.serve_preview(request, mode_name=mode_name)

    def test_render_preview(self):
        self.assertNotContains(self.render_preview(), "o-post-preview")

    def test_render_preview_list_view(self):
        self.assertContains(self.render_preview("list_view"), "o-post-preview")
