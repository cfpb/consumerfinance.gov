import json
from io import StringIO
from unittest.mock import patch

from django.core.cache import cache, caches
from django.template import engines
from django.test import TestCase, override_settings

from scripts import _atomic_helpers as atomic
from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.models.blog_page import BlogPage
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.tests.wagtail_pages.helpers import publish_page


class TestFragmentCacheExtension(ElasticsearchTestsMixin, TestCase):
    def test_cache_gets_called_when_visiting_filterable_page(self):
        # Create a filterable page
        page = BrowseFilterablePage(
            title="test browse filterable page",
            slug="test-browse-filterable-page",
            content=json.dumps([atomic.filter_controls]),
        )
        publish_page(page)

        # Add a child to that filterable page so that there are results
        # with a post preview
        child_page = BlogPage(title="test blog page", slug="test-blog-page")
        page.add_child(instance=child_page)

        self.rebuild_elasticsearch_index("v1", stdout=StringIO())

        cache = caches["post_preview"]
        with patch.object(cache, "add") as add_to_cache:
            # Navigate to the filterable page so that `post-preview.html` loads
            self.client.get("/test-browse-filterable-page/")

            self.assertTrue(add_to_cache.called)


class TestFragmentCacheJinjaTag(TestCase):
    def setUp(self):
        self.jinja_engine = engines["wagtail-env"]

    def tearDown(self):
        cache.clear()

    def _render_tag(self, value, cache_name):
        cache_key = "test-cache-key"

        """Render a template with a single cached value."""
        s = '{%% cache "%s", "%s" %%}{{ value }}{%% endcache %%}' % (
            cache_key,
            cache_name,
        )

        template = self.jinja_engine.from_string(s)
        return template.render({"value": value})

    @override_settings(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            },
        }
    )
    def test_value_that_is_not_cached_gets_rendered_properly(self):
        self.assertEqual(self._render_tag(value="foo", cache_name="default"), "foo")

    @override_settings(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            },
        }
    )
    def test_if_caching_is_disabled_value_always_has_right_value(self):
        value = "foo"
        self._render_tag(value, cache_name="default"),
        value = "bar"
        self.assertEqual(self._render_tag(value, cache_name="default"), "bar")

    @override_settings(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "test-fragment-cache-extension",
            },
        }
    )
    def test_caching_works_properly_if_using_same_cache(self):
        value = "foo"

        # Rendering this value will store False in the cache.
        self._render_tag(value, cache_name="default"),

        value = "bar"

        # Even though the value has changed, we expect the rendering
        # to use the old value because it should read from the cache.
        self.assertEqual(self._render_tag(value, cache_name="default"), "foo")

    @override_settings(
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "test-fragment-cache-extension-1",
            },
            "other": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "test-fragment-cache-extension-2",
            },
        }
    )
    def test_caching_works_properly_if_using_different_caches(self):
        value = "foo"

        # Rendering this value will store 'foo' in the 'default' cache.
        self._render_tag(value, cache_name="default"),

        value = "bar"

        # Because we're using a different cache, rendering the value
        # should return 'bar', because the 'other' cache doesn't know
        # about the previous call.
        self.assertEqual(self._render_tag(value, cache_name="other"), "bar")
