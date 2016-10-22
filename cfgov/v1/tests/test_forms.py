import datetime, mock

from django.db.models import Q
from django.test import TestCase
from django.test.client import RequestFactory

from ..forms import *


class TestFilterableListForm(TestCase):

    # def setUp(self):
    #     rf = RequestFactory()
    #     self.mock_request = {
    #         'saving': rf.post('/admin/pages/' + str(self.page.specific.id) + '/edit', {}),
    #         'sharing': rf.post('/admin/pages/' + str(self.page.specific.id) + '/edit', {'action-share': True}),
    #         'publishing': rf.post('/admin/pages/' + str(self.page.specific.id) + '/edit', {'action-publish': True}),
    #     }
    #     for key in self.mock_request.keys():
    #         self.mock_request[key].user = mock.Mock()


    @mock.patch('v1.forms.FilterableListForm.__init__')
    @mock.patch('taggit.models.Tag.objects')
    def test_set_topics_filters_tags_on_pageids(self, mock_tag_objects, mock_init):
        mock_init.return_value = None
        page_ids = [1, 2, 3, 4, 5]
        form = FilterableListForm()
        form.fields = {'topics': mock.Mock()}
        form.set_topics(page_ids=page_ids)
        mock_tag_objects.filter.assert_called_with(v1_cfgovtaggedpages_items__content_object__id__in=page_ids)


    @mock.patch('v1.forms.FilterableListForm.__init__')
    @mock.patch('taggit.models.Tag.objects')
    def test_set_authors_filters_tags_on_pageids(self, mock_tag_objects, mock_init):
        mock_init.return_value = None
        page_ids = [1, 2, 3, 4, 5]
        form = FilterableListForm()
        form.fields = {'authors': mock.Mock()}
        form.set_authors(page_ids=page_ids)
        mock_tag_objects.filter.assert_called_with(v1_cfgovauthoredpages_items__content_object__id__in=page_ids)


    @mock.patch('v1.forms.FilterableListForm.__init__')
    @mock.patch('__builtin__.super')
    def test_clean_returns_cleaned_data_if_valid(self, mock_super, mock_init):
        mock_init.return_value = None
        from_date = datetime.date.today()
        to_date = from_date + datetime.timedelta(days=1)

        form = FilterableListForm()
        mock_super().clean.return_value = {'from_date': from_date, 'to_date': to_date}
        form.cleaned_data = {'from_date': from_date, 'to_date': to_date}

        result = form.clean()
        assert result['from_date'] == from_date
        assert result['to_date'] == to_date


    @mock.patch('v1.forms.FilterableListForm.__init__')
    @mock.patch('__builtin__.super')
    def test_clean_returns_cleaned_data_if_only_one_date_field_is_empty(self, mock_super, mock_init):
        mock_init.return_value = None
        from_date = datetime.date.today()
        to_date = ''

        form = FilterableListForm()
        mock_super().clean.return_value = {'from_date': from_date, 'to_date': to_date}
        form.cleaned_data = {'from_date': from_date, 'to_date': to_date}

        result = form.clean()
        assert result['from_date'] == from_date
        assert result['to_date'] == to_date


    @mock.patch('v1.forms.FilterableListForm.__init__')
    @mock.patch('__builtin__.super')
    def test_clean_returns_cleaned_data_if_both_date_fields_are_empty(self, mock_super, mock_init):
        mock_init.return_value = None
        from_date = ''
        to_date = ''

        form = FilterableListForm()
        mock_super().clean.return_value = {'from_date': from_date, 'to_date': to_date}
        form.cleaned_data = {'from_date': from_date, 'to_date': to_date}

        result = form.clean()
        assert result['from_date'] == from_date
        assert result['to_date'] == to_date


    @mock.patch('v1.forms.FilterableListForm.__init__')
    @mock.patch('__builtin__.super')
    def test_clean_switches_date_fields_if_todate_is_less_than_fromdate(self, mock_super, mock_init):
        mock_init.return_value = None
        to_date = datetime.date.today()
        from_date = to_date + datetime.timedelta(days=1)

        form = FilterableListForm()
        mock_super().clean.return_value = {'from_date': from_date, 'to_date': to_date}
        form.cleaned_data = {'from_date': from_date, 'to_date': to_date}
        form.data = {'from_date': from_date, 'to_date': to_date}

        result = form.clean()
        assert result['from_date'] == to_date
        assert result['to_date'] == from_date


    # TODO: Fix these from breaking

    # @mock.patch('v1.forms.FilterableListForm.set_field_html_name')
    # @mock.patch('v1.forms.FilterableListForm.__init__')
    # def test_render_with_id_calls_update_to_replace_tag_attr_id(self, mock_init, mock_set_field_html_name):
    #     mock_init.return_value = None
    #     form = FilterableListForm()
    #     field = mock.Mock()
    #     field.fieldname = 'field'
    #     form.fields = {field.fieldname: mock.Mock()}
    #     mock_field = mock.Mock(html_name=field.fieldname)
    #     attr_id = 'foobar'

    #     form.render_with_id(mock_field, attr_id)
    #     assert form.fields[field.fieldname].widget.attrs.update.assert_called_with({'id': attr_id})


    # @mock.patch('v1.forms.FilterableListForm.set_field_html_name')
    # @mock.patch('v1.forms.FilterableListForm.__init__')
    # def test_render_with_id_calls_set_field_html_name_with_field_and_new_id(self, mock_init, mock_set_field_html_name):
    #     mock_init.return_value = None
    #     form = FilterableListForm()
    #     field = mock.Mock()
    #     field.fieldname = 'field'
    #     form.fields = {field.fieldname: mock.Mock()}
    #     mock_field = mock.Mock(html_name=field.fieldname)
    #     attr_id = 'foobar'

    #     form.render_with_id(mock_field, attr_id)
    #     assert mock_set_field_html_name.assert_called_with(form.fields[field.fieldname], attr_id)


    @mock.patch('v1.forms.FilterableListForm.__init__')
    def test_generate_query_returns_empty_query_for_unbound_form(self, mock_init):
        mock_init.return_value = None
        form = FilterableListForm()
        form.is_bound = False

        result = form.generate_query()
        assert result.children == []


    @mock.patch('v1.forms.FilterableListForm.get_query_strings')
    @mock.patch('v1.forms.FilterableListForm.__init__')
    def test_generate_query_returns_empty_query_fields_not_in_cleaned_data(self, mock_init, mock_get_query_strings):
        mock_init.return_value = None
        form = FilterableListForm()
        form.is_bound = True
        form.declared_fields = ['field']
        mock_get_query_strings.return_value = ['field__contains']
        form.cleaned_data = {'notthefield': None}

        result = form.generate_query()
        assert result.children == []


    @mock.patch('v1.forms.FilterableListForm.get_query_strings')
    @mock.patch('v1.forms.FilterableListForm.__init__')
    def test_generate_query_returns_query_from_cleaned_data_fields_and_query_strings(self, mock_init, mock_get_query_strings):
        mock_init.return_value = None
        form = FilterableListForm()
        form.is_bound = True
        form.declared_fields = ['field']
        mock_get_query_strings.return_value = ['field__contains']
        form.cleaned_data = {'field': 'foobar'}

        result = form.generate_query()
        assert result.children == [('field__contains', 'foobar')]

