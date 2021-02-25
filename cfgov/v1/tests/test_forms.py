import datetime
from unittest import mock

from django.test import TestCase

from v1.forms import FilterableDateField, FilterableListForm


class TestFilterableListForm(TestCase):

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
    @mock.patch('builtins.super')
    def test_clean_returns_cleaned_data_if_valid(self, mock_super, mock_init):
        mock_init.return_value = None
        from_date = datetime.date(2017, 7, 4)
        to_date = from_date + datetime.timedelta(days=1)
        form_data = {'from_date': from_date, 'to_date': to_date}

        form = FilterableListForm()
        mock_super().clean.return_value = form_data
        form.cleaned_data = form_data
        form.data = {'from_date': '7/4/2017', 'to_date': '7/5/2017'}
        form._errors = {}

        result = form.clean()
        assert result['from_date'] == from_date
        assert result['to_date'] == to_date

    @mock.patch('v1.forms.FilterableListForm.first_page_date')
    @mock.patch('v1.forms.FilterableListForm.__init__')
    @mock.patch('builtins.super')
    def test_clean_uses_earliest_result_if_fromdate_field_is_empty(self, mock_super, mock_init, mock_pub_date):
        mock_init.return_value = None
        from_date = None
        to_date = datetime.date(2017, 1, 15)
        form_data = {'from_date': from_date, 'to_date': to_date}

        form = FilterableListForm()
        mock_super().clean.return_value = form_data
        form.cleaned_data = form_data
        form.data = {'to_date': '1-15-2017'}
        form._errors = {}
        mock_pub_date.return_value = datetime.date(1995, 1, 1)

        result = form.clean()
        assert result['from_date'] == datetime.date(1995, 1, 1)
        assert result['to_date'] == to_date

    @mock.patch('v1.forms.FilterableListForm.__init__')
    @mock.patch('builtins.super')
    def test_clean_uses_today_if_todate_field_is_empty(self, mock_super, mock_init):
        mock_init.return_value = None
        from_date = datetime.date(2016, 5, 15)
        to_date = None
        form_data = {'from_date': from_date, 'to_date': to_date}

        form = FilterableListForm()
        mock_super().clean.return_value = form_data
        form.cleaned_data = form_data
        form.data = {'from_date': '5-15-2016'}
        form._errors = {}

        result = form.clean()
        assert result['from_date'] == from_date
        assert result['to_date'] == datetime.date.today()

    @mock.patch('v1.forms.FilterableListForm.__init__')
    @mock.patch('builtins.super')
    def test_clean_returns_cleaned_data_if_both_date_fields_are_empty(self, mock_super, mock_init):
        mock_init.return_value = None
        from_date = None
        to_date = None

        form = FilterableListForm()
        mock_super().clean.return_value = {'from_date': from_date, 'to_date': to_date}
        form.cleaned_data = {'from_date': from_date, 'to_date': to_date}
        form.data = {}
        form._errors = {}

        result = form.clean()
        assert result['from_date'] == from_date
        assert result['to_date'] == to_date


    @mock.patch('v1.forms.FilterableListForm.__init__')
    @mock.patch('builtins.super')
    def test_clean_switches_date_fields_if_todate_is_less_than_fromdate(self, mock_super, mock_init):
        mock_init.return_value = None
        to_date = datetime.date(2000, 3, 15)
        from_date = to_date + datetime.timedelta(days=1)

        form = FilterableListForm()
        mock_super().clean.return_value = {'from_date': from_date, 'to_date': to_date}
        form.cleaned_data = {'from_date': from_date, 'to_date': to_date}
        form.data = {'from_date': '3/16/2000', 'to_date': '3/15/2000'}
        form._errors = {}

        result = form.clean()
        assert result['from_date'] == to_date
        assert result['to_date'] == from_date

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


class TestFilterableDateField(TestCase):
    def test_default_required(self):
        field = FilterableDateField()
        self.assertFalse(field.required)

    def test_set_required(self):
        field = FilterableDateField(required=True)
        self.assertTrue(field.required)
