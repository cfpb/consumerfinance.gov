from datetime import date, datetime
from io import StringIO

from django.test import TestCase, override_settings

from wagtail.models import Site

from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.documents import (
    EnforcementActionFilterablePagesDocumentSearch,
    EventFilterablePagesDocumentSearch,
    FilterablePagesDocument,
    FilterablePagesDocumentSearch,
)
from v1.forms import (
    EnforcementActionsFilterForm,
    EventArchiveFilterForm,
    FilterableListForm,
)
from v1.models import (
    BlogPage,
    CFGOVPageCategory,
    EnforcementActionPage,
    EventPage,
)
from v1.tests.wagtail_pages.helpers import publish_page
from v1.util.categories import clean_categories


try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo


class TestFilterableListForm(ElasticsearchTestsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.blog1 = BlogPage(title="test page")
        cls.blog1.categories.add(CFGOVPageCategory(name="foo"))
        cls.blog1.categories.add(CFGOVPageCategory(name="bar"))
        cls.blog1.tags.add("foo")
        cls.blog1.language = "es"
        cls.blog2 = BlogPage(title="another test page")
        cls.blog2.categories.add(CFGOVPageCategory(name="bar"))
        cls.blog2.tags.add("blah")
        cls.category_blog = BlogPage(title="Category Test")
        cls.category_blog.categories.add(
            CFGOVPageCategory(name="info-for-consumers")
        )
        cls.event1 = EventPage(
            title="test page 2",
            start_dt=datetime.now(zoneinfo.ZoneInfo("UTC")),
        )
        cls.event1.tags.add("bar")
        cls.cool_event = EventPage(
            title="Cool Event", start_dt=datetime.now(zoneinfo.ZoneInfo("UTC"))
        )
        cls.awesome_event = EventPage(
            title="Awesome Event",
            start_dt=datetime.now(zoneinfo.ZoneInfo("UTC")),
        )
        publish_page(cls.blog1)
        publish_page(cls.blog2)
        publish_page(cls.event1)
        publish_page(cls.cool_event)
        publish_page(cls.awesome_event)
        publish_page(cls.category_blog)
        cls.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

    def setUpFilterableForm(self, data=None):
        site_root = Site.objects.get(is_default_site=True).root_page
        form = FilterableListForm(
            filterable_search=FilterablePagesDocumentSearch(site_root)
        )
        form.is_bound = True
        form.cleaned_data = data
        return form

    def test_filter_by_category(self):
        form = self.setUpFilterableForm(data={"categories": ["foo"]})
        page_set = form.get_page_set()
        self.assertEqual(page_set.count(), 1)
        self.assertEqual(page_set.to_queryset()[0].specific, self.blog1)

    def test_filter_by_nonexisting_category(self):
        form = self.setUpFilterableForm(data={"categories": ["test filter"]})
        page_set = form.get_page_set()
        self.assertFalse(page_set.count())

    def test_filter_by_tags(self):
        form = self.setUpFilterableForm(data={"topics": ["foo", "bar"]})
        qs = form.get_page_set().to_queryset().specific()
        self.assertEqual(qs.count(), 2)
        self.assertIn(self.blog1, qs)
        self.assertIn(self.event1, qs)

    def test_filter_doesnt_return_drafts(self):
        page2 = BlogPage(title="test page 2")
        page2.tags.add("foo")
        # Don't publish new page
        form = self.setUpFilterableForm(data={"topics": ["foo"]})
        page_set = form.get_page_set()
        self.assertEqual(page_set.count(), 1)
        self.assertEqual(page_set.to_queryset()[0].specific, self.blog1)

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
        self.assertEqual(page_set.count(), 1)
        self.assertEqual(page_set.to_queryset()[0].specific, self.blog1)

    def test_filter_by_title(self):
        form = self.setUpFilterableForm(data={"title": "Cool"})
        page_set = form.get_page_set()
        self.assertEqual(page_set.count(), 1)
        self.assertEqual(page_set.to_queryset()[0].specific, self.cool_event)

    def test_validate_date_after_1900_can_pass(self):
        form = self.setUpFilterableForm()
        form.data = {"from_date": "1/1/1900"}
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
                "policy-compliance",
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
                "issue-spotlight",
            ],
        )

    def test_first_page_date(self):
        form = self.setUpFilterableForm()
        self.assertEqual(form.first_page_date(), self.blog1.date_published)
        form.all_filterable_results = []
        self.assertEqual(form.first_page_date(), date(2010, 1, 1))

    def test_get_topics_sorts_alphabetically(self):
        form = self.setUpFilterableForm()

        self.assertEqual(
            list(form.get_filterable_topics([self.blog1.pk])),
            [("foo", "foo")],
        )

        self.assertEqual(
            list(form.get_filterable_topics([self.blog1.pk, self.blog2.pk])),
            [("blah", "blah"), ("foo", "foo")],
        )


@override_settings(OPENSEARCH_DSL_AUTOSYNC=True)
class TestEventArchiveFilterForm(ElasticsearchTestsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

        event = EventPage(
            title="test page 2",
            start_dt=datetime.now(zoneinfo.ZoneInfo("UTC")),
        )
        event.tags.add("bar")
        publish_page(event)
        cls.event = event

    def test_event_archive_elasticsearch(self):
        site_root = Site.objects.get(is_default_site=True).root_page
        form = EventArchiveFilterForm(
            filterable_search=EventFilterablePagesDocumentSearch(site_root),
        )
        form.is_bound = True
        form.cleaned_data = {"categories": []}
        page_set = form.get_page_set()
        self.assertEqual(page_set.count(), 1)
        self.assertEqual(page_set.to_queryset()[0].specific, self.event)


class TestEnforcementActionsFilterForm(ElasticsearchTestsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        enforcement = EnforcementActionPage(title="Enforcement Action")
        publish_page(enforcement)
        cls.enforcement = enforcement

        cls.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

    def test_enforcement_action_elasticsearch(self):
        site_root = Site.objects.get(is_default_site=True).root_page
        form = EnforcementActionsFilterForm(
            filterable_search=EnforcementActionFilterablePagesDocumentSearch(
                site_root
            ),
        )
        form.is_bound = True
        form.cleaned_data = {"categories": [], "statuses": [], "products": []}
        page_set = form.get_page_set()
        self.assertEqual(page_set.count(), 1)
        self.assertEqual(page_set.to_queryset()[0].specific, self.enforcement)
