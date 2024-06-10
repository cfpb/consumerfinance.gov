from io import StringIO

from django.test import TestCase

from wagtail.models import Page, Site

from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.documents import FilterablePagesDocument
from v1.forms import EventArchiveFilterForm
from v1.models import CFGOVPageCategory, LandingPage
from v1.models.browse_filterable_page import (
    EventArchivePage,
    NewsroomLandingPage,
)
from v1.models.learn_page import AbstractFilterPage
from v1.util.ref import get_category_children


class EventArchivePageTestCase(TestCase):
    def test_get_form_class(self):
        self.assertEqual(
            EventArchivePage.get_form_class(), EventArchiveFilterForm
        )


class TestNewsroomLandingPage(ElasticsearchTestsMixin, TestCase):
    def setUp(self):
        self.newsroom_page = NewsroomLandingPage(
            title="News", slug="newsroom", filter_children_only=False
        )
        self.about_us_page = LandingPage(title="About us", slug="about-us")
        self.site_root = Site.objects.get(is_default_site=True).root_page
        self.site_root.add_child(instance=self.about_us_page)
        self.about_us_page.add_child(instance=self.newsroom_page)
        self.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

    def test_eligible_categories(self):
        self.assertEqual(
            get_category_children(NewsroomLandingPage.filterable_categories),
            [
                "consumer-advisories",
                "directors-statement",
                "letter",
                "op-ed",
                "press-release",
                "speech",
                "testimony",
            ],
        )

    def test_no_pages_by_default(self):
        filterable_search = self.newsroom_page.get_filterable_search()
        result = filterable_search.search()
        self.assertFalse(result.count())

    def make_page_with_category(self, category_name, parent):
        page = AbstractFilterPage(title="test", slug="test")
        parent.add_child(instance=page)

        category = CFGOVPageCategory.objects.create(
            name=category_name, page=page
        )
        page.categories.add(category)
        self.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

    def test_no_pages_matching_categories(self):
        self.make_page_with_category("test", parent=self.site_root)

        filterable_search = self.newsroom_page.get_filterable_search()
        result = filterable_search.search()
        self.assertFalse(result.count())

    def test_page_matches_categories(self):
        self.make_page_with_category("op-ed", parent=self.site_root)

        filterable_search = self.newsroom_page.get_filterable_search()
        result = filterable_search.search()
        self.assertTrue(result.count())

    def test_page_in_other_site_not_included(self):
        wagtail_root = Page.objects.get(pk=1)
        self.make_page_with_category("op-ed", parent=wagtail_root)

        filterable_search = self.newsroom_page.get_filterable_search()
        result = filterable_search.search()
        self.assertFalse(result.count())
