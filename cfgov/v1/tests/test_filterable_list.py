import mock
from django.test import RequestFactory, TestCase

from v1.forms import FilterableListForm

from ..util.filterable_list import FilterableListMixin


class TestFilterableListMixin(TestCase):
    def setUp(self):
        self.mixin = FilterableListMixin()
        self.factory = RequestFactory()
    
    # FilterableListMixin.per_page_limit tests
    def test_per_page_limit_returns_integer(self):
        assert isinstance(self.mixin.per_page_limit(), int)

    def test_get_form_specific_filter_data_returns_GET_data(self):
        request_string = '/?filter_title=test'
        data = self.mixin.get_form_specific_filter_data(self.factory.get(request_string).GET)
        assert data[0]['title'] == 'test'

    def test_get_form_specific_filter_data_returns_GET_data_as_list_for_multiple_values(self):
        request_string = '/?filter_categories=test1&filter_categories=test2'
        data = self.mixin.get_form_specific_filter_data(self.factory.get(request_string).GET)
        assert data[0]['categories'] == ['test1', 'test2']

    # FilterableListMixin.get_context tests
    def test_get_context_raises_exception_for_super_obj_has_no_get_context(self):
        self.assertRaises(AttributeError, self.mixin.get_context, request=self.factory.get('/'))

    @mock.patch('__builtin__.super')
    @mock.patch('v1.util.util.get_secondary_nav_items')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.process_forms')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_forms')
    def test_get_context_calls_super(self, mock_get_forms, mock_process_forms, mock_nav, mock_super):
        self.mixin.get_context(self.factory.get('/'))
        assert mock_super.called

    @mock.patch('__builtin__.super')
    @mock.patch('v1.util.util.get_secondary_nav_items')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.process_forms')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_forms')
    def test_get_context_adds_get_secondary_nav_items_into_context(self, mock_get_forms, mock_process_forms, mock_nav, mock_super):
        mock_super().get_context.return_value = {}
        assert 'get_secondary_nav_items' in self.mixin.get_context(self.factory.get('/'))

    @mock.patch('__builtin__.super')
    @mock.patch('v1.util.util.get_secondary_nav_items')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.process_forms')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_forms')
    def test_get_context_adds_filter_data_into_context(self, mock_get_forms, mock_process_forms, mock_nav, mock_super):
        mock_super().get_context.return_value = {}
        assert 'filter_data' in self.mixin.get_context(self.factory.get('/'))

    # FilterableListMixin.process_forms tests
    @mock.patch('v1.util.filterable_list.FilterableListMixin.per_page_limit')
    def test_process_forms_returns_dictionary_of_forms_and_page_sets(self, mock_per_page_limit):
        data = self.mixin.process_forms(self.factory.get('/'), [])
        assert 'forms' in data
        assert 'page_sets' in data


    @mock.patch('v1.util.filterable_list.Paginator')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.per_page_limit')
    def test_process_forms_calls_is_valid_on_each_form(self, mock_per_page_limit, mock_paginator):
        mock_request = mock.Mock()
        mock_request.GET = self.factory.get('/').GET
        mock_forms = [mock.Mock(), mock.Mock()]
        data = self.mixin.process_forms(mock_request, mock_forms)
        assert mock_forms[0].is_valid.called
        assert mock_forms[1].is_valid.called
