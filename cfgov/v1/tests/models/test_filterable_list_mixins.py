from io import StringIO
from unittest import mock

from django.test import RequestFactory, TestCase, override_settings

from wagtail.core.blocks import StreamValue
from wagtail.core.models import Site, Page

from scripts._atomic_helpers import filter_controls
from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.models import BlogPage
from v1.models.browse_filterable_page import BrowseFilterablePage
from v1.models.filterable_list_mixins import FilterableListMixin


class TestFilterableListMixin(TestCase):

    def setUp(self):
        self.mixin = FilterableListMixin()
        self.factory = RequestFactory()

    # FilterableListMixin.filterable_per_page_limit tests
    def test_per_page_limit_returns_integer(self):
        self.assertIsInstance(
            FilterableListMixin.filterable_per_page_limit,
            int
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
        self
    ):
        self.assertRaises(
            AttributeError,
            self.mixin.get_context,
            request=self.factory.get("/")
        )

    @mock.patch("v1.models.filterable_list_mixins.Paginator")
    def test_process_form_calls_is_valid_on_each_form(self, mock_paginator):
        mock_request = mock.Mock()
        mock_request.GET = self.factory.get("/").GET
        mock_form = mock.Mock()
        self.mixin.process_form(mock_request, mock_form)
        assert mock_form.is_valid.called

    def test_filterable_pages_not_in_site_returns_no_pages(self):
        class MockPageInDefaultSite(FilterableListMixin):
            def get_site(self):
                return None

        self.assertFalse(
            MockPageInDefaultSite().get_filterable_queryset().exists()
        )

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


class FilterableListContextTestCase(ElasticsearchTestsMixin, TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.filterable_page = BrowseFilterablePage(title="Blog", slug="test")
        self.root = Site.objects.get(is_default_site=True).root_page
        self.home_page = Page(title="Home")
        self.root.add_child(instance=self.home_page)
        self.home_page.add_child(instance=self.filterable_page)
        self.page = BlogPage(title="Child test page", live=True)
        self.archived_page = BlogPage(
            title="Archive test page",
            live=True,
            is_archived='yes'
        )
        self.filterable_page.add_child(instance=self.page)
        self.filterable_page.add_child(instance=self.archived_page)

        self.rebuild_elasticsearch_index('v1', stdout=StringIO())

    def test_get_context_has_archived_posts(self):
        context = self.filterable_page.get_context(
            request=self.factory.get("/test/")
        )
        self.assertTrue(context['has_archived_posts'])

    @override_settings(
        FLAGS={"HIDE_ARCHIVE_FILTER_OPTIONS": [("boolean", True)]}
    )
    def test_get_context_has_archived_posts_with_hide_archive_flag_on(self):
        context = self.filterable_page.get_context(
            request=self.factory.get("/test/")
        )
        self.assertFalse(context['has_archived_posts'])


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

        self.rebuild_elasticsearch_index('v1', stdout=StringIO())

    def test_index_route(self):
        response = self.client.get("/test/")
        self.assertEqual(
            response.context_data["filter_data"]["page_set"][0].title,
            "Test"
        )

    def test_feed_route(self):
        response = self.client.get("/test/feed/")
        self.assertEqual(
            response["content-type"],
            "application/rss+xml; charset=utf-8"
        )


class FilterableListRelationsTestCase(ElasticsearchTestsMixin, TestCase):

    def setUp(self):
        self.filter_controls = filter_controls

        self.filterable_page = BrowseFilterablePage(title="Blog", slug="test")
        self.root = Site.objects.get(is_default_site=True).root_page
        self.home_page = Page(title="Home")
        self.root.add_child(instance=self.home_page)
        self.home_page.add_child(instance=self.filterable_page)

        self.set_filterable_controls(filter_controls)

        self.child_page = BlogPage(title="Child test page", live=True)
        self.sibling_page = BlogPage(title="Sibling test page", live=True)
        self.archived_sibling_page = BlogPage(
            title="Archive test page",
            live=True,
            is_archived='yes'
        )
        self.filterable_page.add_child(instance=self.child_page)
        self.filterable_page.get_parent().add_child(instance=self.sibling_page)
        self.filterable_page.get_parent().add_child(
            instance=self.archived_sibling_page
        )

        self.rebuild_elasticsearch_index('v1', stdout=StringIO())

    def set_filterable_controls(self, value):
        self.filterable_page.content = StreamValue(
            self.filterable_page.content.stream_block,
            [value],
            True
        )
        self.filterable_page.save()

    def test_get_filterable_children_pages(self):
        filter_controls['value']['filter_children'] = True
        filter_controls['value']['filter_siblings'] = False
        self.set_filterable_controls(self.filter_controls)

        qs = self.filterable_page.get_filterable_queryset()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].pk, self.child_page.pk)
        self.assertEqual("/home/", self.filterable_page.get_filterable_root())

    def test_get_filterable_root_site_wide(self):
        filter_controls['value']['filter_children'] = False
        filter_controls['value']['filter_siblings'] = False
        self.set_filterable_controls(self.filter_controls)

        root = self.filterable_page.get_filterable_root()
        self.assertEqual("/", root)
