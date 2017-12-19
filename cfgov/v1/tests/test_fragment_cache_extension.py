from django.core.cache import caches
from django.test import Client, TestCase

from wagtail.wagtailcore.blocks import StreamValue

from mock import patch
from scripts import _atomic_helpers as atomic

from v1.models.blog_page import BlogPage
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.tests.wagtail_pages.helpers import (
    publish_changes, publish_page, save_new_page
)


django_client = Client()
cache = caches['post_preview']

class TestFragmentCacheExtension(TestCase):

    @patch.object(cache, 'add')
    def test_cache_gets_called_when_visiting_filterable_page(self, add_to_cache):
        # Create a filterable page
        page = BrowseFilterablePage(
            title='test browse filterable page',
            slug='test-browse-filterable-page'
        )
        page.content = StreamValue(
            page.content.stream_block,
            [atomic.filter_controls],
            True
        )
        publish_page(page)

        # Add a child to that filterable page so that there are related posts results
        child_page = BlogPage(
            title='test blog page',
            slug='test-blog-page'
        )
        page.add_child(instance=child_page)

        # Navigate to the filterable page so that `post-preview.html` loads
        django_client.get('/test-browse-filterable-page/')

        self.assertTrue(add_to_cache.called)
