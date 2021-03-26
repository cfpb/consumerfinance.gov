from django.test import RequestFactory, TestCase

from wagtail.core.models import Site

from v1.models import BlogPage, SublandingFilterablePage
from v1.tests.wagtail_pages.helpers import save_new_page


class BlogPageTests(TestCase):
    def test_unpublished_page_doesnt_include_rss_feed(self):
        page = BlogPage(title='test', slug='test')

        request = RequestFactory().get('/')
        response = page.serve(request)

        self.assertNotContains(response, 'RSS feed')

    def test_page_includes_rss_feed_of_parent(self):
        parent_page = SublandingFilterablePage(title='test', slug='test')
        save_new_page(parent_page)

        child_page = BlogPage(title='test', slug='test')
        save_new_page(child_page, root=parent_page)

        response = self.client.get('/test/test/')
        self.assertContains(response, 'href="/test/feed/')
