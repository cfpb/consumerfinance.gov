import logging
from collections import Counter

from django import forms
from django.db.models import Q
from django.forms import widgets
from django.forms.utils import ErrorList
from taggit.models import Tag

from util import ERROR_MESSAGES
from v1.util import ref
from v1.util.categories import clean_categories

from .models.base import CFGOVPage, Feedback
from .models.learn_page import AbstractFilterPage

logger = logging.getLogger(__name__)


class FilterErrorList(ErrorList):
    def __str__(self):
        return '\n'.join(str(e) for e in self)


class FilterDateField(forms.DateField):
    def clean(self, value):
        from sheerlike.templates import get_date_obj
        if value:
            try:
                value = get_date_obj(value)
            except Exception:
                pass
        return value


class PDFFilterDateField(forms.DateField):
    def clean(self, value):
        from sheerlike.templates import get_date_string
        if value:
            try:
                value = get_date_string(value)
            except Exception:
                pass
        return value


class FilterCheckboxList(forms.CharField):
    def validate(self, value):
        if value in self.empty_values and self.required:
            msg = self.error_messages['required']
            if self.label and '%s' in msg:
                msg = msg % self.label
            raise forms.ValidationError(msg, code='required')


class CalenderPDFFilterForm(forms.Form):
    filter_calendar = FilterCheckboxList(
        label='Calendar',
        error_messages=ERROR_MESSAGES['CHECKBOX_ERRORS']
    )
    filter_range_date_gte = PDFFilterDateField(
        required=False,
        error_messages=ERROR_MESSAGES['DATE_ERRORS']
    )
    filter_range_date_lte = PDFFilterDateField(
        required=False,
        error_messages=ERROR_MESSAGES['DATE_ERRORS']
    )

    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = FilterErrorList
        super(CalenderPDFFilterForm, self).__init__(*args, **kwargs)

    def clean_filter_calendar(self):
        return self.cleaned_data['filter_calendar'].replace(' ', '+')

    def clean(self):
        cleaned_data = super(CalenderPDFFilterForm, self).clean()
        from_date_empty = 'filter_range_date_gte' in cleaned_data and \
                          cleaned_data['filter_range_date_gte'] is None
        to_date_empty = 'filter_range_date_lte' in cleaned_data and \
                        cleaned_data['filter_range_date_lte'] is None

        if from_date_empty and to_date_empty:
            raise forms.ValidationError(
                ERROR_MESSAGES['DATE_ERRORS']['one_required']
            )
        return cleaned_data


class MultipleChoiceFieldNoValidation(forms.MultipleChoiceField):
    def validate(self, value):
        pass


class FilterableListForm(forms.Form):
    title_attrs = {
        'placeholder': 'Search for a specific word in item title'
    }
    topics_select_attrs = {
        'multiple': 'multiple',
        'data-placeholder': 'Search for topics',
    }
    authors_select_attrs = {
        'multiple': 'multiple',
        'data-placeholder': 'Search for authors'
    }
    from_select_attrs = {
        'class': 'js-filter_range-date js-filter_range-date__gte',
        'type': 'text',
        'placeholder': 'mm/dd/yyyy',
        'data-type': 'date'
    }
    to_select_attrs = from_select_attrs.copy()
    to_select_attrs.update({
        'class': 'js-filter_range-date js-filter_range-date__lte',
    })

    title = forms.CharField(
        max_length=250,
        required=False,
        widget=widgets.TextInput(attrs=title_attrs)
    )
    from_date = FilterDateField(
        required=False,
        input_formats=['%m/%d/%Y'],
        widget=widgets.DateInput(attrs=from_select_attrs)
    )
    to_date = FilterDateField(
        required=False,
        input_formats=['%m/%d/%Y'],
        widget=widgets.DateInput(attrs=to_select_attrs)
    )
    categories = forms.MultipleChoiceField(
        required=False,
        choices=ref.page_type_choices,
        widget=widgets.CheckboxSelectMultiple()
    )
    topics = MultipleChoiceFieldNoValidation(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(attrs=topics_select_attrs)
    )
    authors = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(attrs=authors_select_attrs)
    )

    def __init__(self, *args, **kwargs):
        self.hostname = kwargs.pop('hostname')
        self.base_query = kwargs.pop('base_query')
        super(FilterableListForm, self).__init__(*args, **kwargs)
        page_ids = CFGOVPage.objects.live_shared(
            self.hostname
        ).values_list('id', flat=True)

        clean_categories(selected_categories=self.data.get('categories'))
        self.set_topics(page_ids)
        self.set_authors(page_ids)

    def base_query(self):
        base_query = AbstractFilterPage.objects.live_shared(
            hostname=self.hostname)
        if self.parent:
            base_query = base_query.filter(
                CFGOVPage.objects.child_of_q(self.parent))
            logger.info('Filtering by parent {}'.format(self.parent))
        return base_query

    def get_page_set(self):
        query = self.generate_query()
        return self.base_query.filter(query).distinct().order_by(
            '-date_published'
        )

    def prepare_options(self, arr):
        """
        Returns an ordered list of tuples of the format
        ('tag-slug-name', 'Tag Display Name')
        """
        arr = Counter(arr).most_common()  # Order by most to least common
        # Grab only the first tuple in the generated tuple,
        # which includes a count we do not need
        return [x[0] for x in arr]

    # Populate Topics' choices
    def set_topics(self, page_ids):
        tags = Tag.objects.filter(
            v1_cfgovtaggedpages_items__content_object__id__in=page_ids
        ).values_list('slug', 'name')

        options = self.prepare_options(arr=tags)
        most = options[:3]
        other = options[3:]

        self.fields['topics'].choices = \
            (('Most frequent', most),
             ('All other topics', other))

    # Populate Authors' choices
    def set_authors(self, page_ids):
        authors = Tag.objects.filter(
            v1_cfgovauthoredpages_items__content_object__id__in=page_ids
        ).values_list('slug', 'name')
        options = self.prepare_options(arr=authors)

        self.fields['authors'].choices = options

    def clean(self):
        cleaned_data = super(FilterableListForm, self).clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        # Check if both date_lte and date_gte are present
        # If the 'start' date is after the 'end' date, swap them
        if (from_date and to_date) and to_date < from_date:
            data = dict(self.data)
            data_to_date = data['to_date']
            self.cleaned_data['to_date'], data['to_date'] = \
                from_date, data['from_date']
            self.cleaned_data['from_date'], data['from_date'] = \
                to_date, data_to_date
            self.data = data
        return self.cleaned_data

    # Does the job of {{ field }}
    # In the template, you pass the field and the id and name you'd like to
    # render the field with.
    def render_with_id(self, field, attr_id):
        for f in self.fields:
            if field.html_name == f:
                self.fields[f].widget.attrs.update({'id': attr_id})
                self.set_field_html_name(self.fields[f], attr_id)
                return self[f]

    # Sets the html name by replacing the render method to use the given name.
    def set_field_html_name(self, field, new_name):
        """
        This creates wrapper around the normal widget rendering,
        allowing for a custom field name (new_name).
        """
        old_render = field.widget.render
        if isinstance(field.widget, widgets.SelectMultiple):
            field.widget.render = lambda name, value, attrs=None, choices=(): \
                old_render(new_name, value, attrs, choices)
        else:
            field.widget.render = lambda name, value, attrs=None: \
                old_render(new_name, value, attrs)

    # Generates a query by iterating over the zipped collection of
    # tuples.
    def generate_query(self):
        final_query = Q()
        if self.is_bound:
            for query, field_name in zip(
                self.get_query_strings(),
                self.declared_fields
            ):
                if self.cleaned_data.get(field_name):
                    final_query &= \
                        Q((query, self.cleaned_data.get(field_name)))
        return final_query

    # Returns a list of query strings to associate for each field, ordered by
    # the field declaration for the form. Note: THEY MUST BE ORDERED IN THE
    # SAME WAY AS THEY ARE DECLARED IN THE FORM DEFINITION.
    def get_query_strings(self):
        return [
            'title__icontains',      # title
            'date_published__gte',   # from_date
            'date_published__lte',   # to_date
            'categories__name__in',  # categories
            'tags__slug__in',        # topics
            'authors__slug__in',     # authors
        ]


class EventArchiveFilterForm(FilterableListForm):
    def get_query_strings(self):
        return [
            'title__icontains',      # title
            'start_dt__gte',         # from_date
            'end_dt__lte',           # to_date
            'categories__name__in',  # categories
            'tags__slug__in',        # topics
            'authors__slug__in',     # authors
        ]


class FeedbackForm(forms.ModelForm):
    """For feedback modules that simply ask 'Was this page helfpul?'"""
    class Meta:
        model = Feedback
        fields = ['is_helpful', 'comment']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['is_helpful'].required = True


class ReferredFeedbackForm(forms.ModelForm):
    """For feedback modules that need to capture the referring page"""
    class Meta:
        model = Feedback
        fields = ['is_helpful', 'referrer', 'comment']

    def __init__(self, *args, **kwargs):
        super(ReferredFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = True


class SuggestionFeedbackForm(forms.ModelForm):
    """For feedback modules seeking content suggestions"""

    class Meta:
        model = Feedback
        fields = ['referrer',
                  'comment',
                  'expect_to_buy',
                  'currently_own',
                  'email']

    def __init__(self, *args, **kwargs):
        super(SuggestionFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = True
