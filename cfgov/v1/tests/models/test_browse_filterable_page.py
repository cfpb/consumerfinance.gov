from io import StringIO

from django.test import TestCase

from wagtail.core.models import Page, Site

from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.forms import EventArchiveFilterForm
from v1.models import CFGOVPageCategory, LandingPage
from v1.models.browse_filterable_page import (
    NEWSROOM_CACHE_TAG, EventArchivePage, NewsroomLandingPage
)
from v1.models.learn_page import AbstractFilterPage
from v1.util.ref import get_category_children


class EventArchivePageTestCase(TestCase):
    def test_get_form_class(self):
        self.assertEqual(
            EventArchivePage.get_form_class(),
            EventArchiveFilterForm
        )


class TestNewsroomLandingPage(ElasticsearchTestsMixin, TestCase):
    def setUp(self):
        self.newsroom_page = NewsroomLandingPage(title="News", slug='newsroom')
        self.about_us_page = LandingPage(title="About us", slug="about-us")
        self.site_root = Site.objects.get(is_default_site=True).root_page
        self.site_root.add_child(instance=self.about_us_page)
        self.about_us_page.add_child(instance=self.newsroom_page)
        self.rebuild_elasticsearch_index('v1', stdout=StringIO())

    def test_eligible_categories(self):
        self.assertEqual(
            get_category_children(NewsroomLandingPage.filterable_categories),
            [
                'consumer-advisories',
                'directors-statement',
                'op-ed',
                'press-release',
                'speech',
                'testimony',
            ]
        )

    def test_no_pages_by_default(self):
        filterable_search = self.newsroom_page.get_filterable_search()
        result = filterable_search.search()
        self.assertFalse(result.exists())

    def make_page_with_category(self, category_name, parent):
        page = AbstractFilterPage(title='test', slug='test')
        parent.add_child(instance=page)

        category = CFGOVPageCategory.objects.create(
            name=category_name,
            page=page
        )
        page.categories.add(category)
        self.rebuild_elasticsearch_index('v1', stdout=StringIO())

    def test_no_pages_matching_categories(self):
        self.make_page_with_category('test', parent=self.site_root)

        filterable_search = self.newsroom_page.get_filterable_search()
        result = filterable_search.search()
        self.assertFalse(result.exists())

    def test_page_matches_categories(self):
        self.make_page_with_category('op-ed', parent=self.site_root)

        filterable_search = self.newsroom_page.get_filterable_search()
        result = filterable_search.search()
        self.assertTrue(result.exists())

    def test_page_in_other_site_not_included(self):
        wagtail_root = Page.objects.get(pk=1)
        self.make_page_with_category('op-ed', parent=wagtail_root)

        filterable_search = self.newsroom_page.get_filterable_search()
        result = filterable_search.search()
        self.assertFalse(result.exists())

    def test_cache_tag_applied(self):
        self.newsroom_page.save_revision().publish()
        response = self.client.get(self.newsroom_page.url)
        self.assertEqual(response.get("Edge-Cache-Tag"), NEWSROOM_CACHE_TAG)
