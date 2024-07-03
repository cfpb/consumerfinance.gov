import json
from io import StringIO
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from wagtail.models import Page, Site

from dateutil.relativedelta import relativedelta

from core.testutils.test_cases import WagtailPageTreeTestCase
from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.documents import (
    EnforcementActionFilterablePagesDocumentSearch,
    EventFilterablePagesDocumentSearch,
    FilterablePagesDocument,
    FilterablePagesDocumentSearch,
)
from v1.models import (
    AbstractFilterPage,
    BlogPage,
    CFGOVPageCategory,
    DocumentDetailPage,
    EnforcementActionPage,
    EnforcementActionProduct,
    EnforcementActionStatus,
    EventPage,
    SublandingFilterablePage,
)


class FilterablePagesDocumentTest(TestCase):
    def test_model_class_added(self):
        self.assertEqual(
            FilterablePagesDocument.django.model, AbstractFilterPage
        )

    def test_ignore_signal_default(self):
        self.assertFalse(FilterablePagesDocument.django.ignore_signals)

    def test_auto_refresh_default(self):
        self.assertFalse(FilterablePagesDocument.Index.auto_refresh)

    def test_fields_populated(self):
        mapping = FilterablePagesDocument._doc_type.mapping
        self.assertCountEqual(
            mapping.properties.properties.to_dict().keys(),
            [
                "model_class",
                "path",
                "depth",
                "title",
                "live",
                "start_date",
                "end_date",
                "language",
                "tags",
                "categories",
                "statuses",
                "products",
                "content",
            ],
        )

    def test_get_queryset(self):
        test_event = EventPage(title="Testing", start_dt=timezone.now())
        qs = FilterablePagesDocument().get_queryset()
        self.assertFalse(qs.filter(title=test_event.title).exists())

    def test_prepare_statuses(self):
        enforcement = EnforcementActionPage(
            title="Great Test Page",
            initial_filing_date=timezone.now(),
        )
        status = EnforcementActionStatus(status="expired-terminated-dismissed")
        enforcement.statuses.add(status)
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(enforcement)
        self.assertEqual(
            prepared_data["statuses"], ["expired-terminated-dismissed"]
        )

    def test_prepare_content_no_content_defined(self):
        event = EventPage(title="Event Test", start_dt=timezone.now())
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(event)
        self.assertIsNone(prepared_data["content"])

    def test_prepare_content_exists(self):
        blog = BlogPage(
            title="Test Blog",
            content=json.dumps(
                [
                    {
                        "type": "full_width_text",
                        "value": [
                            {
                                "type": "content",
                                "value": "Blog Text",
                            },
                        ],
                    },
                ]
            ),
        )
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(blog)
        self.assertEqual(prepared_data["content"], "Blog Text")

    def test_prepare_content_empty(self):
        blog = BlogPage(title="Test Blog", content=json.dumps([]))
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(blog)
        self.assertIsNone(prepared_data["content"])

    def test_prepare_products(self):
        enforcement = EnforcementActionPage(
            title="Great Test Page",
            initial_filing_date=timezone.now(),
        )
        product = EnforcementActionProduct(product="Fair Lending")
        enforcement.products.add(product)
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(enforcement)
        self.assertEqual(prepared_data["products"], ["Fair Lending"])


class ElasticsearchWagtailPageTreeTestCase(
    ElasticsearchTestsMixin, WagtailPageTreeTestCase
):
    """Test case that creates and indexes a Wagtail page tree."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )


class FilterableSearchTests(ElasticsearchWagtailPageTreeTestCase):
    @classmethod
    def get_page_tree(cls):
        return [
            (
                SublandingFilterablePage(title="search1"),
                [
                    DocumentDetailPage(title="child1"),
                    DocumentDetailPage(title="child2"),
                    (
                        SublandingFilterablePage(title="search2"),
                        [
                            DocumentDetailPage(title="nested child1"),
                            DocumentDetailPage(title="nested child2"),
                        ],
                    ),
                ],
            )
        ]

    def test_search_from_root(self):
        # By default search only returns AbstractFilterPages
        # that are direct children of the specified root.
        search = FilterablePagesDocumentSearch(self.page_tree[0])
        self.assertEqual(search.count(), 2)

    def test_search_children_only(self):
        # Setting children_only to False returns all AbstractFilterablePages
        # that live anywhere underneath the specified root.
        search = FilterablePagesDocumentSearch(
            self.page_tree[0], children_only=False
        )
        self.assertEqual(search.count(), 4)

    def test_search_from_other_page(self):
        # Search works starting from some other page in the tree.
        page = Page.objects.get(slug="search2")
        search = FilterablePagesDocumentSearch(page)
        self.assertEqual(search.count(), 2)

    def test_search_by_title(self):
        search = FilterablePagesDocumentSearch(
            self.page_tree[0], children_only=False
        )
        self.assertEqual(search.search(title="child").count(), 4)
        self.assertEqual(search.search(title="child1").count(), 2)
        self.assertEqual(search.search(title="child3").count(), 0)

    def test_get_raw_results(self):
        search = FilterablePagesDocumentSearch(self.page_tree[0])
        results = search.get_raw_results()
        self.assertEqual(len(results.hits), 2)

    # Mocking is necessary here because unfortunately it's not currently
    # possible to use override_settings with DOD autosync. See
    # https://github.com/django-es/django-elasticsearch-dsl/issues/322.
    @patch(
        "django_opensearch_dsl.apps.DODConfig.autosync_enabled",
        return_value=True,
    )
    def test_index_updates_automatically(self, _):
        search = FilterablePagesDocumentSearch(self.page_tree[0])
        self.assertEqual(search.search(title="foo").count(), 0)
        indexed_page = Page.objects.get(slug="child1").specific
        indexed_page.title = "child1 foo"
        indexed_page.save_revision().publish()
        self.assertEqual(search.search(title="foo").count(), 1)

    # Mocking is necessary here because unfortunately it's not currently
    # possible to use override_settings with DOD autosync. See
    # https://github.com/django-es/django-elasticsearch-dsl/issues/322.
    @patch(
        "django_opensearch_dsl.apps.DODConfig.autosync_enabled",
        return_value=True,
    )
    def test_search_excludes_not_live_pages(self, _):
        child = DocumentDetailPage(title="child3", live=False)
        self.page_tree[0].add_child(instance=child)

        # This is a no-op but triggers indexing of this non-live page.
        child.move(self.page_tree[0], pos="last-child")

        search = FilterablePagesDocumentSearch(self.page_tree[0])
        self.assertEqual(search.count(), 2)


class FilterableSearchFilteringTests(
    ElasticsearchTestsMixin, WagtailPageTreeTestCase
):
    @classmethod
    def get_page_tree(cls):
        cls.today = timezone.now().date()
        cls.yesterday = cls.today - relativedelta(days=1)

        return [
            (
                SublandingFilterablePage(title="search"),
                [
                    BlogPage(
                        title="en",
                        language="en",
                        date_published=cls.today,
                    ),
                    BlogPage(
                        title="es",
                        language="es",
                        date_published=cls.yesterday,
                    ),
                ],
            ),
        ]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Page tags and categories can't be set at creation time, so they need
        # to be added after the page tree has been created.
        def add_tag_and_category_to_page(page_slug, name):
            page = BlogPage.objects.get(slug=page_slug)
            page.tags.add(name)
            page.categories.add(CFGOVPageCategory(name=name))
            page.save()

        add_tag_and_category_to_page("en", "foo")
        add_tag_and_category_to_page("es", "bar")

        cls.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

    def test_no_filters(self):
        search = FilterablePagesDocumentSearch(self.page_tree[0])
        self.assertEqual(search.count(), 2)

        search.filter()
        self.assertEqual(search.count(), 2)

    def test_filter_by_language(self):
        search = FilterablePagesDocumentSearch(self.page_tree[0])
        self.assertEqual(search.count(), 2)

        search.filter_language(["es"])
        self.assertEqual(search.count(), 1)

    def test_filter_by_date(self):
        search = FilterablePagesDocumentSearch(self.page_tree[0])
        search.filter_date(from_date=self.today, to_date=self.today)
        self.assertEqual(search.count(), 1)

        search = FilterablePagesDocumentSearch(self.page_tree[0])
        search.filter_date(from_date=self.yesterday, to_date=self.yesterday)
        self.assertEqual(search.count(), 1)

    def test_filter_by_topics(self):
        search = FilterablePagesDocumentSearch(self.page_tree[0])
        search.filter_topics(["foo"])
        self.assertEqual(search.count(), 1)

    def test_filter_by_categories(self):
        search = FilterablePagesDocumentSearch(self.page_tree[0])
        search.filter_categories(["bar"])
        self.assertEqual(search.count(), 1)


class EnforcementActionFilterableSearchFilteringTests(
    ElasticsearchTestsMixin, WagtailPageTreeTestCase
):
    @classmethod
    def get_page_tree(cls):
        cls.today = timezone.now().date()
        cls.yesterday = cls.today - relativedelta(days=1)

        return [
            (
                SublandingFilterablePage(title="search1"),
                [
                    EnforcementActionPage(
                        title="child1", initial_filing_date=cls.yesterday
                    ),
                    EnforcementActionPage(
                        title="child2", initial_filing_date=cls.today
                    ),
                    DocumentDetailPage(title="should be ignored"),
                ],
            ),
        ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Page status and products can't be set at creation time, so they need
        # to be added after the page tree has been created.
        page = EnforcementActionPage.objects.get(slug="child1")
        status = EnforcementActionStatus(status="expired-terminated-dismissed")
        page.statuses.add(status)
        product = EnforcementActionProduct(product="Debt Collection")
        page.products.add(product)
        page.save()

        cls.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

    def test_no_filters(self):
        search = EnforcementActionFilterablePagesDocumentSearch(
            self.page_tree[0], ordering="-start_date"
        )
        search.filter()
        results = search.search()

        # The EA search default filter behavior excludes pages that are not of
        # type EnforcementActionPage.
        self.assertEqual(results.count(), 2)

        # Results should be ordered by most recent initial filing date.
        qs = results.to_queryset()
        self.assertEqual(qs[0].title, "child2")
        self.assertEqual(qs[1].title, "child1")

    def test_filter_by_status(self):
        search = EnforcementActionFilterablePagesDocumentSearch(
            self.page_tree[0]
        )
        search.filter(statuses=["expired-terminated-dismissed"])
        self.assertEqual(search.count(), 1)

    def test_filter_by_product(self):
        search = EnforcementActionFilterablePagesDocumentSearch(
            self.page_tree[0]
        )

        search.filter(products=["Debt Collection"])
        self.assertEqual(search.count(), 1)

    def test_filter_by_date(self):
        search = EnforcementActionFilterablePagesDocumentSearch(
            self.page_tree[0]
        )
        search.filter(from_date=self.today, to_date=self.today)
        self.assertEqual(search.count(), 1)

        search = EnforcementActionFilterablePagesDocumentSearch(
            self.page_tree[0]
        )
        search.filter(from_date=self.yesterday, to_date=self.yesterday)
        self.assertEqual(search.count(), 1)


class EventFilterableSearchFilteringTests(
    ElasticsearchWagtailPageTreeTestCase
):
    @classmethod
    def get_page_tree(cls):
        cls.now = timezone.now()
        cls.one_hour_ago = cls.now - relativedelta(hours=1)
        cls.one_day_ago = cls.now - relativedelta(days=1)

        return [
            (
                SublandingFilterablePage(title="search1"),
                [
                    EventPage(
                        title="child1",
                        start_dt=cls.one_day_ago,
                        end_dt=cls.one_hour_ago,
                    ),
                    EventPage(
                        title="child2",
                        start_dt=cls.one_hour_ago,
                        end_dt=cls.now,
                    ),
                    DocumentDetailPage(title="should be ignored"),
                ],
            ),
        ]

    def test_no_filters(self):
        search = EventFilterablePagesDocumentSearch(self.page_tree[0])
        search.filter()
        results = search.search()

        # The event search default filter behavior excludes pages that are not
        # of type EventPage.
        self.assertEqual(results.count(), 2)

    def test_filter_by_date(self):
        search = EventFilterablePagesDocumentSearch(self.page_tree[0])
        search.filter(from_date=self.one_day_ago)
        self.assertEqual(search.count(), 2)

        search = EventFilterablePagesDocumentSearch(self.page_tree[0])
        search.filter(from_date=self.now + relativedelta(days=1))
        self.assertEqual(search.count(), 0)

        search = EventFilterablePagesDocumentSearch(self.page_tree[0])
        search.filter(to_date=self.now)
        self.assertEqual(search.count(), 2)

        search = EventFilterablePagesDocumentSearch(self.page_tree[0])
        search.filter(to_date=self.one_day_ago - relativedelta(days=1))
        self.assertEqual(search.count(), 0)

        search = EventFilterablePagesDocumentSearch(self.page_tree[0])
        search.filter(from_date=self.one_day_ago, to_date=self.now)
        self.assertEqual(search.count(), 2)

        search = EventFilterablePagesDocumentSearch(self.page_tree[0])
        search.filter(from_date=self.one_day_ago, to_date=self.one_day_ago)
        self.assertEqual(search.count(), 1)


class TestThatWagtailPageSignalsUpdateIndex(ElasticsearchTestsMixin, TestCase):
    def test_index_reflects_page_moves_and_deletions(self):
        root = Site.objects.get(is_default_site=True).root_page

        parent = BlogPage(title="parent", live=True)
        root.add_child(instance=parent)

        blog1 = BlogPage(title="foo 1", live=True)
        parent.add_child(instance=blog1)

        blog2 = BlogPage(title="foo 2", live=True)
        parent.add_child(instance=blog2)

        blog3 = BlogPage(title="foo 3", live=True)
        parent.add_child(instance=blog3)

        self.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )
        search = FilterablePagesDocumentSearch(parent)

        # Initially a search at the root should return 3 results.
        results = search.search(title="foo")
        self.assertEqual(results.count(), 3)

        # By default we set OPENSEARCH_DSL_AUTOSYNC to False in
        # settings.test, and there's unfortunately no better way to override
        # that here than by patching; see
        # https://github.com/django-es/django-elasticsearch-dsl/issues/322.
        with patch(
            "django_opensearch_dsl.apps.DODConfig.autosync_enabled",
            return_value=True,
        ):
            # Moving a page out of the parent should update the index so that
            # a search there now returns only 2 results.
            blog2.move(root)
            results = search.search(title="foo")
            self.assertEqual(results.count(), 2)

            # Updating a page should also update the index so that a search
            # now returns only 1 result.
            blog3.title = "bar"
            blog3.save_revision().publish()
            results = search.search(title="foo")
            self.assertEqual(results.count(), 1)

            # Deleting the remaining page with "blog" in the root should
            # result in an empty search result.
            blog1.delete()
            results = search.search(title="foo")
            self.assertEqual(results.count(), 0)
