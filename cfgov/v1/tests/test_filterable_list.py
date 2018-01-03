from django.test import RequestFactory, TestCase

import mock

from v1.forms import FilterableListForm

from ..util.filterable_list import FilterableListMixin


class TestFilterableListMixin(TestCase):
    def setUp(self):
        self.mixin = FilterableListMixin()
        self.factory = RequestFactory()
    
    # FilterableListMixin.per_page_limit tests
    def test_per_page_limit_returns_integer(self):
        assert isinstance(self.mixin.per_page_limit(), int)

    def test_get_form_data_returns_GET_data(self):
        request_string = '/?title=test'
        data = self.mixin.get_form_data(self.factory.get(request_string).GET)
        assert data[0]['title'] == 'test'

    def test_get_form_data_returns_GET_data_as_list_for_multiple_values(self):
        request_string = '/?categories=test1&categories=test2'
        data = self.mixin.get_form_data(self.factory.get(request_string).GET)
        assert data[0]['categories'] == ['test1', 'test2']

    # FilterableListMixin.get_context tests
    def test_get_context_raises_exception_for_super_obj_has_no_get_context(self):
        self.assertRaises(AttributeError, self.mixin.get_context, request=self.factory.get('/'))

    @mock.patch('v1.util.filterable_list.Paginator')
    @mock.patch('v1.util.filterable_list.FilterableListMixin.per_page_limit')
    def test_process_form_calls_is_valid_on_each_form(self, mock_per_page_limit, mock_paginator):
        mock_request = mock.Mock()
        mock_request.GET = self.factory.get('/').GET
        mock_form = mock.Mock()
        data = self.mixin.process_form(mock_request, mock_form)
        assert mock_form.is_valid.called
