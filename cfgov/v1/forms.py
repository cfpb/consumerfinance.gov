from util import ERROR_MESSAGES

from django import forms
from django.db.models import Q
from django.forms.utils import ErrorList
from django.forms import widgets

from sheerlike.templates import date_formatter
from v1.models import CFGOVPage
from .models import ref


class FilterErrorList(ErrorList):
    def __str__(self):
        return '\n'.join(str(e) for e in self)


class FilterDateField(forms.DateField):
    def clean(self, value):
        if value:
            try:
                value = date_formatter(value)
            except Exception as e:
                pass
        return value


class FilterCheckboxList(forms.CharField):
    def validate(self, value):
        if value in self.empty_values and self.required:
            print value
            msg = self.error_messages['required']
            if self.label and '%s' in msg:
                msg = msg % self.label
            raise forms.ValidationError(msg, code='required')


class CalenderPDFFilterForm(forms.Form):
    filter_calendar = FilterCheckboxList(label='Calendar',
        error_messages=ERROR_MESSAGES['CHECKBOX_ERRORS'])
    filter_range_date_gte = FilterDateField(required=False,
        error_messages=ERROR_MESSAGES['DATE_ERRORS'])
    filter_range_date_lte = FilterDateField(required=False,
        error_messages=ERROR_MESSAGES['DATE_ERRORS'])

    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = FilterErrorList
        super(CalenderPDFFilterForm, self).__init__(*args, **kwargs)

    def clean_filter_calendar(self):
        return self.cleaned_data['filter_calendar'].replace(' ', '+')

    def clean(self):
        cleaned_data = super(CalenderPDFFilterForm, self).clean()
        from_date_empty = 'filter_range_date_gte' in cleaned_data and \
                          cleaned_data['filter_range_date_gte']  == None
        to_date_empty = 'filter_range_date_lte' in cleaned_data and \
                        cleaned_data['filter_range_date_lte'] == None

        if from_date_empty and to_date_empty :
            raise forms.ValidationError(ERROR_MESSAGES['DATE_ERRORS']['one_required'])
        return cleaned_data


class FilterForm(forms.Form):
    topics_select_attrs = {
        'class': 'chosen-select',
        'multiple': 'multiple',
        'data-placeholder': 'Search for topics',
    }
    authors_select_attrs = {
        'class': 'chosen-select',
        'multiple': 'multiple',
        'data-placeholder': 'Search for authors',
    }
    from_select_attrs = {
        'class': 'js-filter_range-date js-filter_range-date__gte',
        'type': 'text',
        'placeholder': 'dd/mm/yyyy',
    }
    to_select_attrs = from_select_attrs.copy()
    to_select_attrs.update({
        'class': 'js-filter_range-date js-filter_range-date__lte',
    })

    from_date = FilterDateField(
        required=False,
        input_formats=['%d/%m/%Y'],
        widget=widgets.DateInput(attrs=from_select_attrs))
    to_date = FilterDateField(
        required=False,
        input_formats=['%d/%m/%Y'],
        widget=widgets.DateInput(attrs=to_select_attrs))
    categories = forms.MultipleChoiceField(
        required=False,
        choices=ref.page_type_choices,
        widget=widgets.CheckboxSelectMultiple())
    topics = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(attrs=topics_select_attrs))
    authors = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(attrs=authors_select_attrs))
    title = forms.CharField(max_length=250, required=False)

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        # Populate Topics' choices
        topics_options = list(set([tag for tags in [page.tags.names() for page
                                   in CFGOVPage.objects.live()]
                                   for tag in tags]))
        most = [(option, option) for option in topics_options[:3]]
        other = [(option, option) for option in topics_options[3:]]
        self.fields['topics'].choices = \
            (('Most frequent', tuple(most)),
             ('All other topics', tuple(other)))

        # Populate Authors' choices
        self.fields['authors'].choices = \
            list(set([author for authors in [page.authors.names() for page
                      in CFGOVPage.objects.live()] for author in authors]))

    def clean(self):
        cleaned_data = super(FilterForm, self).clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        # Check if both date_lte and date_gte are present
        # If the 'start' date is after the 'end' date, swap them
        if (from_date and to_date) and to_date < from_date:
            data = dict(self.data)
            self.cleaned_data['to_date'], data['to_date'] = \
                from_date, from_date
            self.cleaned_data['from_date'], data['from_date'] = \
                to_date, to_date
            self.data = data
        return self.cleaned_data

    def render_with_id(self, field, attr_id):
        for f in self.fields:
            if field.html_name in f:
                self.fields[f].widget.attrs.update({'id': attr_id})
                self.set_field_html_name(self.fields[f], attr_id)
                return self[f]

    def set_field_html_name(self, field, new_name):
        """
        This creates wrapper around the normal widget rendering,
        allowing for a custom field name (new_name).
        """
        old_render = field.widget.render
        field.widget.render = \
            lambda name, value, attrs=None: old_render(new_name, value, attrs)

    def generate_query(self):
        final_query = Q()
        if self.is_bound:
            for query, field_name in self.field_query_map():
                if self.cleaned_data.get(field_name):
                    final_query &= \
                        Q((query, self.cleaned_data.get(field_name)))
        return final_query

    def field_query_map(self):
        return zip(
            [
                'date_published__gte',
                'date_published__lte',
                'categories__name__in',
                'tags__name__in',
                'authors__name__in',
                'title__icontains',
            ],
            [
                'from_date',
                'to_date',
                'categories',
                'topics',
                'authors',
                'title',
            ]
        )
