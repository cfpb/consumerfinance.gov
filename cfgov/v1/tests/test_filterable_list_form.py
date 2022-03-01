from datetime import date, datetime
from io import StringIO

from django.test import TestCase, override_settings

from pytz import timezone

from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.documents import (
    EnforcementActionFilterablePagesDocumentSearch,
    EventFilterablePagesDocumentSearch,
    FilterablePagesDocumentSearch,
)
from v1.forms import (
    EnforcementActionsFilterForm,
    EventArchiveFilterForm,
    FilterableListForm,
)
from v1.models import BlogPage
from v1.models.base import CFGOVPageCategory
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.models.learn_page import EventPage
from v1.tests.wagtail_pages.helpers import publish_page
from v1.util.categories import clean_categories


class TestFilterableListForm(ElasticsearchTestsMixin, TestCase):
    def setUp(self):
        self.blog1 = BlogPage(title="test page")
        self.blog1.categories.add(CFGOVPageCategory(name="foo"))
        self.blog1.categories.add(CFGOVPageCategory(name="bar"))
        self.blog1.tags.add("foo")
        self.blog1.authors.add("richa-agarwal")
        self.blog1.language = "es"
        self.blog2 = BlogPage(title="another test page")
        self.blog2.categories.add(CFGOVPageCategory(name="bar"))
        self.blog2.tags.add("blah")
        self.blog2.authors.add("richard-cordray")
        self.category_blog = BlogPage(title="Category Test")
        self.category_blog.categories.add(
            CFGOVPageCategory(name="info-for-consumers")
        )
        self.event1 = EventPage(
            title="test page 2", start_dt=datetime.now(timezone("UTC"))
        )
        self.event1.tags.add("bar")
        self.cool_event = EventPage(
            title="Cool Event", start_dt=datetime.now(timezone("UTC"))
        )
        self.awesome_event = EventPage(
            title="Awesome Event", start_dt=datetime.now(timezone("UTC"))
        )
        publish_page(self.blog1)
        publish_page(self.blog2)
        publish_page(self.event1)
        publish_page(self.cool_event)
        publish_page(self.awesome_event)
        publish_page(self.category_blog)
        self.rebuild_elasticsearch_index("v1", stdout=StringIO())

    def setUpFilterableForm(self, data=None, filterable_categories=None):
        form = FilterableListForm(
            filterable_search=FilterablePagesDocumentSearch(prefix="/"),
            wagtail_block=None,
            filterable_categories=filterable_categories,
        )
        form.is_bound = True
        form.cleaned_data = data
        return form

    def test_filter_by_category(self):
        form = self.setUpFilterableForm(data={"categories": ["foo"]})
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.blog1)

    def test_filter_by_nonexisting_category(self):
        form = self.setUpFilterableForm(data={"categories": ["test filter"]})
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 0)

    def test_filter_by_tags(self):
        form = self.setUpFilterableForm(data={"topics": ["foo", "bar"]})
        page_set_pks = form.get_page_set().values_list("pk", flat=True)
        self.assertEqual(len(page_set_pks), 2)
        self.assertIn(self.blog1.pk, page_set_pks)
        self.assertIn(self.event1.pk, page_set_pks)

    def test_filter_doesnt_return_drafts(self):
        page2 = BlogPage(title="test page 2")
        page2.tags.add("foo")
        # Don't publish new page
        form = self.setUpFilterableForm(data={"topics": ["foo"]})
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.blog1)

    def test_form_language_choices(self):
        form = self.setUpFilterableForm()
        self.assertEqual(
            form.fields["language"].choices,
            [
                ("en", "English"),
                ("es", "Spanish"),
            ],
        )

    def test_filter_by_language(self):
        form = self.setUpFilterableForm(data={"language": ["es"]})
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.blog1)

    def test_filter_by_title(self):
        form = self.setUpFilterableForm(data={"title": "Cool"})
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.cool_event)

    def test_validate_date_after_1900_can_pass(self):
        form = self.setUpFilterableForm()
        form.data = {"from_date": "1/1/1900", "archived": "exclude"}
        self.assertTrue(form.is_valid())

    def test_validate_date_after_1900_can_fail(self):
        form = self.setUpFilterableForm()
        form.data = {"from_date": "12/31/1899"}
        self.assertFalse(form.is_valid())
        self.assertIn("from_date", form._errors)

    def test_clean_categories_converts_blog_subcategories_correctly(self):
        form = self.setUpFilterableForm()
        form.data = {"categories": ["blog"]}
        clean_categories(selected_categories=form.data.get("categories"))
        self.assertEqual(
            form.data["categories"],
            [
                "blog",
                "at-the-cfpb",
                "directors-notebook",
                "policy_compliance",
                "data-research-reports",
                "info-for-consumers",
            ],
        )

    def test_clean_categories_converts_reports_subcategories_correctly(self):
        form = self.setUpFilterableForm()
        form.data = {"categories": ["research-reports"]}
        clean_categories(selected_categories=form.data.get("categories"))
        self.assertEqual(
            form.data["categories"],
            [
                "research-reports",
                "consumer-complaint",
                "super-highlight",
                "data-point",
                "industry-markets",
                "consumer-edu-empower",
                "to-congress",
                "data-spotlight",
            ],
        )

    def test_filterable_categories_sets_initial_category_list(self):
        form = self.setUpFilterableForm(
            data={"categories": []},
            filterable_categories=("Blog", "Newsroom", "Research Report"),
        )
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.category_blog)

    def test_first_page_date(self):
        form = self.setUpFilterableForm()
        self.assertEqual(form.first_page_date(), self.blog1.date_published)
        form.all_filterable_results = []
        self.assertEqual(form.first_page_date(), date(2010, 1, 1))


class TestFilterableListFormArchive(ElasticsearchTestsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.page1 = BlogPage(title="test page", is_archived="yes")
        cls.page2 = BlogPage(title="another test page")
        cls.page3 = BlogPage(title="never-archived page", is_archived="never")
        publish_page(cls.page1)
        publish_page(cls.page2)
        publish_page(cls.page3)

        cls.rebuild_elasticsearch_index("v1", stdout=StringIO())

    def get_filtered_pages(self, data):
        form = FilterableListForm(
            filterable_search=FilterablePagesDocumentSearch(prefix="/"),
            wagtail_block=None,
            filterable_categories=None,
            data=data,
        )

        self.assertTrue(form.is_valid())
        return form.get_page_set()

    def test_filter_by_archived_include(self):
        pages = self.get_filtered_pages({"archived": "include"})
        self.assertEqual(len(pages), 3)

    def test_filter_by_archived_exclude(self):
        pages = self.get_filtered_pages({"archived": "exclude"})
        self.assertEqual(len(pages), 2)
        self.assertEqual(pages[0].specific, self.page2)

    def test_filter_by_archived_only(self):
        pages = self.get_filtered_pages({"archived": "only"})
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0].specific, self.page1)


@override_settings(ELASTICSEARCH_DSL_AUTOSYNC=True)
class TestEventArchiveFilterForm(ElasticsearchTestsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rebuild_elasticsearch_index("v1", stdout=StringIO())

        event = EventPage(
            title="test page 2", start_dt=datetime.now(timezone("UTC"))
        )
        event.tags.add("bar")
        publish_page(event)
        cls.event = event

    def test_event_archive_elasticsearch(self):
        form = EventArchiveFilterForm(
            filterable_search=EventFilterablePagesDocumentSearch(prefix="/"),
            wagtail_block=None,
            filterable_categories=None,
        )
        form.is_bound = True
        form.cleaned_data = {"categories": []}
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.event)


class TestEnforcementActionsFilterForm(ElasticsearchTestsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        enforcement = EnforcementActionPage(title="Enforcement Action")
        publish_page(enforcement)
        cls.enforcement = enforcement

        cls.rebuild_elasticsearch_index("v1", stdout=StringIO())

    def test_enforcement_action_elasticsearch(self):
        form = EnforcementActionsFilterForm(
            filterable_search=EnforcementActionFilterablePagesDocumentSearch(
                prefix="/"
            ),
            wagtail_block=None,
            filterable_categories=None,
        )
        form.is_bound = True
        form.cleaned_data = {"categories": [], "statuses": [], "products": []}
        page_set = form.get_page_set()
        self.assertEqual(len(page_set), 1)
        self.assertEqual(page_set[0].specific, self.enforcement)
