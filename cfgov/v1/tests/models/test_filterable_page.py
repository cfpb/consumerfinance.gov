from datetime import date
from io import StringIO
from unittest import mock

from django.test import RequestFactory, TestCase

from wagtail.models import Page, Site

from core.testutils.test_cases import WagtailPageTreeTestCase
from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.documents import FilterablePagesDocument
from v1.models import BlogPage, BrowseFilterablePage, SublandingFilterablePage
from v1.models.filterable_page import AbstractFilterablePage


class TestAbstractFilterablePage(TestCase):
    def setUp(self):
        self.page = BrowseFilterablePage()
        self.factory = RequestFactory()

    # AbstractFilterablePage.filterable_per_page_limit tests
    def test_per_page_limit_returns_integer(self):
        self.assertIsInstance(
            AbstractFilterablePage.filterable_per_page_limit, int
        )

    def test_get_form_data_returns_GET_data(self):
        request_string = "/?title=test"
        data = self.page.get_form_data(self.factory.get(request_string).GET)
        assert data[0]["title"] == "test"

    def test_get_form_data_returns_GET_data_as_list_for_multiple_values(self):
        request_string = "/?categories=test1&categories=test2"
        data = self.page.get_form_data(self.factory.get(request_string).GET)
        assert data[0]["categories"] == ["test1", "test2"]

    def test_do_not_index_is_false_by_default(self):
        assert self.page.do_not_index is False

    def test_do_not_index_is_false_if_no_query(self):
        request_string = ""
        self.page.get_form_data(self.factory.get(request_string).GET)
        assert self.page.do_not_index is False

    def test_do_not_index_is_true_if_query(self):
        request_string = "/?categories=test1&topic=test2"
        self.page.get_form_data(self.factory.get(request_string).GET)
        assert self.page.do_not_index is True

    def test_do_not_index_is_false_if_query_is_single_topic(self):
        request_string = "/?topic=test1"
        self.page.get_form_data(self.factory.get(request_string).GET)
        assert self.page.do_not_index is False

    def test_do_not_index_is_true_if_query_is_multiple_topics(self):
        request_string = "/?topic=test1&topic=test2"
        self.page.get_form_data(self.factory.get(request_string).GET)
        assert self.page.do_not_index is False


class FilterableRoutesTestCase(ElasticsearchTestsMixin, TestCase):
    def setUp(self):
        self.filterable_page = BrowseFilterablePage(title="Blog", slug="test")
        self.root = Site.objects.get(is_default_site=True).root_page
        self.root.add_child(instance=self.filterable_page)

        self.page = BlogPage(
            pk=123,
            title="Test",
            slug="one",
            live=True,
            search_description="A blog post",
            date_published=date(2024, 1, 1),
        )
        self.filterable_page.add_child(instance=self.page)

        self.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

    def test_index_route(self):
        response = self.client.get("/test/")
        self.assertEqual(response.context_data["results"][0]["title"], "Test")

    def test_feed_route(self):
        response = self.client.get("/test/feed/")
        self.assertEqual(
            response["content-type"], "application/rss+xml; charset=utf-8"
        )
        self.assertEqual(response["Edge-Control"], "cache-maxage=10m")

        self.assertContains(
            response,
            (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">'
                "<channel>"
                "<title>Blog | Consumer Financial Protection Bureau</title>"
                "<link>http://localhost/test/</link>"
                "<description/>"
                '<atom:link href="http://testserver/test/feed/" rel="self"/>'
                "<language>en-us</language>"
                "<lastBuildDate>"
                "Mon, 01 Jan 2024 00:00:00 -0500"
                "</lastBuildDate>"
                "<item>"
                "<title>Test</title>"
                "<link>http://localhost/test/one/</link>"
                "<description>A blog post</description>"
                "<pubDate>Mon, 01 Jan 2024 00:00:00 -0500</pubDate>"
                '<guid isPermaLink="false">'
                "123&lt;&gt;consumerfinance.gov"
                "</guid>"
                "</item>"
                "</channel>"
                "</rss>"
            ),
        )

    def test_cache_tag_applied(self):
        response = self.client.get(self.filterable_page.url)
        self.assertEqual(
            response.get("Edge-Cache-Tag"), self.filterable_page.slug
        )

    def test_cache_tag_applied_to_feed(self):
        response = self.client.get(self.filterable_page.url + "feed/")
        self.assertEqual(
            response.get("Edge-Cache-Tag"), self.filterable_page.slug
        )

    def test_x_robots_tag(self):
        response = self.client.get(
            self.filterable_page.url, {"topics": "test1"}
        )
        self.assertIsNone(response.get("X-Robots-Tag"))

        response = self.client.get(self.filterable_page.url, {"title": "test"})
        self.assertEqual(response.get("X-Robots-Tag"), "noindex")


class MockSearch:
    def __init__(self, search_root, children_only, ordering):
        self.search_root = search_root
        self.children_only = children_only
        self.ordering = ordering


@mock.patch(
    "v1.models.BrowseFilterablePage.get_search_class", return_value=MockSearch
)
class FilterableListSearchTestCase(TestCase):
    def test_no_filterable_list_block_defaults(self, _):
        page = BrowseFilterablePage(title="test")

        search = page.get_filterable_search()
        self.assertEqual(search.search_root, page)
        self.assertEqual(search.children_only, True)
        self.assertEqual(
            search.ordering, AbstractFilterablePage.DEFAULT_ORDERING
        )

    def test_search_default_children_only(self, _):
        page = BrowseFilterablePage(title="test")
        search = page.get_filterable_search()
        self.assertEqual(search.search_root, page)
        self.assertEqual(search.children_only, True)
        self.assertEqual(
            search.ordering, AbstractFilterablePage.DEFAULT_ORDERING
        )

    def test_search_children_only_true(self, _):
        page = BrowseFilterablePage(title="test", filter_children_only=True)
        search = page.get_filterable_search()
        self.assertEqual(search.search_root, page)
        self.assertEqual(search.children_only, True)
        self.assertEqual(
            search.ordering, AbstractFilterablePage.DEFAULT_ORDERING
        )

    def test_search_children_only_false_uses_default_site_if_not_in_site(
        self, _
    ):
        page = BrowseFilterablePage(title="test", filter_children_only=False)
        search = page.get_filterable_search()
        self.assertEqual(
            search.search_root,
            Site.objects.get(is_default_site=True).root_page,
        )
        self.assertEqual(search.children_only, False)
        self.assertEqual(
            search.ordering, AbstractFilterablePage.DEFAULT_ORDERING
        )

    def test_search_children_only_false_uses_site_root(self, _):
        page = BrowseFilterablePage(title="test", filter_children_only=False)
        Page.objects.get(pk=1).add_child(instance=page)
        Site.objects.create(root_page=page)

        search = page.get_filterable_search()
        self.assertEqual(search.search_root.specific, page)
        self.assertEqual(search.children_only, False)
        self.assertEqual(
            search.ordering, AbstractFilterablePage.DEFAULT_ORDERING
        )

    def test_search_different_ordering(self, _):
        page = BrowseFilterablePage(title="test", filtered_ordering="title")
        search = page.get_filterable_search()
        self.assertEqual(search.search_root, page)
        self.assertEqual(search.children_only, True)
        self.assertEqual(search.ordering, "title")


class FilterableResultsRenderingTests(
    ElasticsearchTestsMixin, WagtailPageTreeTestCase
):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

    @classmethod
    def get_page_tree(cls):
        return [
            (
                SublandingFilterablePage(title="search"),
                [
                    BlogPage(title="child1"),
                    BlogPage(title="child2"),
                ],
            )
        ]

    def test_render(self):
        page = self.page_tree[0]
        request = RequestFactory().get("/")

        # Page rendering requires 8 database queries in total.
        #
        # 2 are needed for Wagtail page URL generation:
        #
        #   1. Fetching Wagtail Site root paths.
        #   2. Fetching the root page of the default Wagtail Site.
        #
        # 1 is needed to render our filterable form:
        #
        #   3. Retrieving the list of page tags to populate the form topic
        #      choices.
        #
        # 2 are needed to fetch page results from the database:
        #
        #   4. Fetching Page content types based on search result IDs.
        #   5. Fetching specific Page model instances.
        #
        # 3 are needed for efficient page rendering:
        #
        #   6. Prefetching all authors for all result pages.
        #   7. Prefecthing all categories for all result pages.
        #   8. Prefetching all topic tags for all result pages.
        with self.assertNumQueries(8):
            response = page.render(request)

        # All data is fetched as part of the response context. No additional
        # queries are needed to render the results themselves, but there are
        # 2 additional queries for all pages:
        #
        #   1. Fetching the mega menu.
        #   2. Fetching any banners associated with the page.
        with self.assertNumQueries(2):
            response.render()
