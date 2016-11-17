import mock

from django.test import TestCase
from django.test import RequestFactory

from ..util.filterable_list import FilterableListMixin
from v1.forms import FilterableListForm


class TestFilterableListMixin(TestCase):
    def setUp(self):
        self.mixin = FilterableListMixin()
        self.factory = RequestFactory()
    
    # FilterableListMixin.per_page_limit tests
    def test_per_page_limit_returns_integer(self):
        assert isinstance(self.mixin.per_page_limit(), int)


    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_form_specific_filter_data')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_filter_ids')
    def test_has_active_filters_calls_get_form_specific_filter_data(self, mock_get_filter_ids, mock_getspecific):
        self.mixin.has_active_filters(mock.Mock(), mock.Mock())
        assert mock_getspecific.called


    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_form_specific_filter_data')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_filter_ids')
    def test_has_active_filters_calls_get_filter_ids(self, mock_get_filter_ids, mock_getspecific):
        self.mixin.has_active_filters(mock.Mock(), mock.Mock())
        assert mock_get_filter_ids.called


    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_form_specific_filter_data')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_filter_ids')
    def test_has_active_filters_returns_false_for_empty_forms_data(self, mock_get_filter_ids, mock_getspecific):
        mock_getspecific.return_value = None
        assert not self.mixin.has_active_filters(mock.Mock(), mock.Mock())


    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_form_specific_filter_data')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_filter_ids')
    def test_has_active_filters_returns_false_for_forms_data_with_None_values(self, mock_get_filter_ids, mock_getspecific):
        mock_getspecific.return_value = [{'key': None}]
        assert not self.mixin.has_active_filters(mock.Mock(), mock.Mock())


    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_form_specific_filter_data')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_filter_ids')
    def test_has_active_filters_returns_true_for_forms_data_with_values(self, mock_get_filter_ids, mock_getspecific):
        mock_get_filter_ids.return_value = [0]
        mock_getspecific.return_value = [{'key': 'value'}]
        assert self.mixin.has_active_filters(mock.Mock(), 0)


    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_form_specific_filter_data')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_filter_ids')
    def test_has_active_filters_returns_false_for_index_mte_filter_data_length(self, mock_get_filter_ids, mock_getspecific):
        mock_getspecific.return_value = []
        assert not self.mixin.has_active_filters(mock.Mock(), 0)
        assert not self.mixin.has_active_filters(mock.Mock(), 1)


    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_form_specific_filter_data')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_filter_ids')
    def test_has_active_filters_returns_false_for_forms_data_without_values_callable(self, mock_get_filter_ids, mock_getspecific):
        mock_getspecific.return_value = 'no callable `values`'
        assert not self.mixin.has_active_filters(mock.Mock(), 0)


    # FilterableListMixin.get_filter_ids tests
    def test_get_filter_ids_returns_list(self):
        block = mock.Mock()
        block.block_type = 'filter_controls'
        self.mixin.content = [block]
        assert isinstance(self.mixin.get_filter_ids(), list)


    def test_get_filter_ids_returns_list_of_integers(self):
        block = mock.Mock()
        block.block_type = 'filter_controls'
        self.mixin.content = [block]
        for item in self.mixin.get_filter_ids():
            assert isinstance(item, int)


    def test_get_filter_ids_returns_empty_list_when_filter_controls_not_in_blocks(self):
        block = mock.Mock()
        block.block_type = 'nottherighttype'
        self.mixin.content = [block]
        lst = self.mixin.get_filter_ids()
        assert isinstance(lst, list) and not lst


    def test_get_filter_ids_raises_exception_if_blocks_dont_have_block_type(self):
        block = mock.Mock()
        block.block_type = 1 # not a string or iterable
        self.mixin.content = [block]
        self.assertRaises(TypeError, self.mixin.get_filter_ids)

    # FilterableListMixin.get_form_specific_filter_data tests
    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_filter_ids')
    def test_get_form_specific_filter_data_calls_get_filter_ids(self, mock_getfilterids):
        self.mixin.get_form_specific_filter_data(
            mock.Mock())
        assert mock_getfilterids.called

    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_filter_ids')
    def test_get_form_specific_filter_data_returns_GET_data_categorized_by_form_id(self, mock_getfilterids):
        mock_getfilterids.return_value = [0]
        request_string = '/?filter0_title=test'
        data = self.mixin.get_form_specific_filter_data(self.factory.get(request_string).GET)
        assert data[0]['title'] == 'test'

    @mock.patch('v1.util.filterable_list.FilterableListMixin.get_filter_ids')
    def test_get_form_specific_filter_data_returns_GET_data_as_list_for_multiple_values(self, mock_getfilterids):
        mock_getfilterids.return_value = [0]
        request_string = '/?filter0_categories=test1&filter0_categories=test2'
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
