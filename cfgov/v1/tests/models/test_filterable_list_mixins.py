import json
from io import StringIO
from unittest import mock

from django.test import RequestFactory, TestCase

from wagtail.core.models import Page, Site

from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.documents import FilterablePagesDocument
from v1.models import BlogPage, BrowseFilterablePage
from v1.models.filterable_list_mixins import FilterableListMixin


class TestFilterableListMixin(TestCase):
    def setUp(self):
        self.mixin = FilterableListMixin()
        self.factory = RequestFactory()

    # FilterableListMixin.filterable_per_page_limit tests
    def test_per_page_limit_returns_integer(self):
        self.assertIsInstance(
            FilterableListMixin.filterable_per_page_limit, int
        )

    def test_get_form_data_returns_GET_data(self):
        request_string = "/?title=test"
        data = self.mixin.get_form_data(self.factory.get(request_string).GET)
        assert data[0]["title"] == "test"

    def test_get_form_data_returns_GET_data_as_list_for_multiple_values(self):
        request_string = "/?categories=test1&categories=test2"
        data = self.mixin.get_form_data(self.factory.get(request_string).GET)
        assert data[0]["categories"] == ["test1", "test2"]

    # FilterableListMixin.get_context tests
    def test_get_context_raises_exception_for_super_obj_has_no_get_context(
        self,
    ):
        self.assertRaises(
            AttributeError,
            self.mixin.get_context,
            request=self.factory.get("/"),
        )

    @mock.patch("v1.models.filterable_list_mixins.Paginator")
    def test_process_form_calls_is_valid_on_each_form(self, mock_paginator):
        mock_request = mock.Mock()
        mock_request.GET = self.factory.get("/").GET
        mock_form = mock.Mock()
        self.mixin.process_form(mock_request, mock_form)
        assert mock_form.is_valid.called

    # FilterableListMixin.set_do_not_index tests
    def test_do_not_index_is_false_by_default(self):
        assert self.mixin.do_not_index is False

    def test_do_not_index_is_false_if_no_query(self):
        request_string = ""
        self.mixin.get_form_data(self.factory.get(request_string).GET)
        assert self.mixin.do_not_index is False

    def test_do_not_index_is_true_if_query(self):
        request_string = "/?categories=test1&topic=test2"
        self.mixin.get_form_data(self.factory.get(request_string).GET)
        assert self.mixin.do_not_index is True

    def test_do_not_index_is_false_if_query_is_single_topic(self):
        request_string = "/?topic=test1"
        self.mixin.get_form_data(self.factory.get(request_string).GET)
        assert self.mixin.do_not_index is False

    def test_do_not_index_is_true_if_query_is_multiple_topics(self):
        request_string = "/?topic=test1&topic=test2"
        self.mixin.get_form_data(self.factory.get(request_string).GET)
        assert self.mixin.do_not_index is False


class FilterableRoutesTestCase(ElasticsearchTestsMixin, TestCase):
    def setUp(self):
        self.filterable_page = BrowseFilterablePage(title="Blog", slug="test")
        self.root = Site.objects.get(is_default_site=True).root_page
        self.root.add_child(instance=self.filterable_page)

        self.page = BlogPage(
            title="Test",
            slug="one",
            live=True,
        )
        self.filterable_page.add_child(instance=self.page)

        self.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )

    def test_index_route(self):
        response = self.client.get("/test/")
        self.assertEqual(
            response.context_data["filter_data"]["page_set"][0].title, "Test"
        )

    def test_feed_route(self):
        response = self.client.get("/test/feed/")
        self.assertEqual(
            response["content-type"], "application/rss+xml; charset=utf-8"
        )
        self.assertEqual(response["Edge-Control"], "cache-maxage=10m")

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
    def __init__(self, search_root, children_only):
        self.search_root = search_root
        self.children_only = children_only


@mock.patch(
    "v1.models.BrowseFilterablePage.get_search_class", return_value=MockSearch
)
class FilterableListSearchTestCase(TestCase):
    def test_no_filterable_list_block_defaults(self, _):
        page = BrowseFilterablePage(title="test")

        search = page.get_filterable_search()
        self.assertEqual(search.search_root, page)
        self.assertEqual(search.children_only, True)

    def test_search_default_children_only(self, _):
        page = BrowseFilterablePage(
            title="test",
            content=json.dumps(
                [
                    {"type": "filter_controls", "value": {}},
                ]
            ),
        )

        search = page.get_filterable_search()
        self.assertEqual(search.search_root, page)
        self.assertEqual(search.children_only, True)

    def test_search_children_only_true(self, _):
        page = BrowseFilterablePage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "filter_controls",
                        "value": {
                            "filter_children": True,
                        },
                    },
                ]
            ),
        )

        search = page.get_filterable_search()
        self.assertEqual(search.search_root, page)
        self.assertEqual(search.children_only, True)

    def test_search_children_only_false_uses_default_site_if_not_in_site(
        self, _
    ):
        page = BrowseFilterablePage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "filter_controls",
                        "value": {
                            "filter_children": False,
                        },
                    },
                ]
            ),
        )

        search = page.get_filterable_search()
        self.assertEqual(
            search.search_root,
            Site.objects.get(is_default_site=True).root_page,
        )
        self.assertEqual(search.children_only, False)

    def test_search_children_only_false_uses_site_root(self, _):
        page = BrowseFilterablePage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "filter_controls",
                        "value": {
                            "filter_children": False,
                        },
                    },
                ]
            ),
        )

        Page.objects.get(pk=1).add_child(instance=page)
        Site.objects.create(root_page=page)

        search = page.get_filterable_search()
        self.assertEqual(search.search_root.specific, page)
        self.assertEqual(search.children_only, False)
