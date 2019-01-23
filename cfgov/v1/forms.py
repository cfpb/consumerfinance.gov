from collections import Counter
from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import widgets

from taggit.models import Tag

from v1.util import ERROR_MESSAGES, ref
from v1.util.categories import clean_categories
from v1.util.date_filter import end_of_time_period

from .models.base import Feedback


class MultipleChoiceFieldNoValidation(forms.MultipleChoiceField):
    def validate(self, value):
        pass


class FilterableDateField(forms.DateField):
    def validate_after_1900(date):
        strftime_earliest_year = 1900
        if date.year < strftime_earliest_year:
            raise ValidationError("Please enter a date of 1/1/1900 or later.")

    default_validators = [validate_after_1900]

    default_input_formats = (
        '%m/%d/%y',     # 10/25/16, 9/1/16
        '%m-%d-%y',     # 10-25-16, 9-1-16
        '%m/%d/%Y',     # 10/25/2016, 9/1/2016
        '%m-%d-%Y',     # 10-25-2016, 9-1-2016
        '%m/%Y',        # 10/2016, 7/2017
        '%m-%Y',        # 10-2016, 7-2017
        '%m/%y',        # 10/16, 4/18
        '%m-%y',        # 10-16, 4-18
        '%Y',           # 2016
    )

    default_widget_attrs = {
        'class': 'a-text-input a-text-input__full',
        'type': 'text',
        'placeholder': 'mm/dd/yyyy',
        'data-type': 'date'
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        kwargs.setdefault('input_formats', self.default_input_formats)
        kwargs.setdefault('error_messages', ERROR_MESSAGES['DATE_ERRORS'])

        field_id = kwargs.pop('field_id', None)
        if field_id:
            self.default_widget_attrs['id'] = field_id

        kwargs.setdefault('widget', widgets.DateInput(
            attrs=self.default_widget_attrs
        ))
        super(FilterableDateField, self).__init__(*args, **kwargs)


class FilterableListForm(forms.Form):
    title = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'o-filterable-list-controls_title',
            'class': 'a-text-input a-text-input__full',
            'placeholder': 'Search for a specific word in item title',
        })
    )
    from_date = FilterableDateField(
        field_id='o-filterable-list-controls_from-date'
    )

    to_date = FilterableDateField(
        field_id='o-filterable-list-controls_to-date'
    )

    categories = forms.MultipleChoiceField(
        required=False,
        choices=ref.page_type_choices,
        widget=widgets.CheckboxSelectMultiple()
    )

    topics = MultipleChoiceFieldNoValidation(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_topics',
            'class': 'o-multiselect',
            'data-placeholder': 'Search for topics',
            'multiple': 'multiple',
        })
    )

    authors = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_authors',
            'class': 'o-multiselect',
            'data-placeholder': 'Search for authors',
            'multiple': 'multiple',
        })
    )

    preferred_datetime_format = '%m/%d/%Y'

    def __init__(self, *args, **kwargs):
        self.filterable_pages = kwargs.pop('filterable_pages')
        super(FilterableListForm, self).__init__(*args, **kwargs)

        clean_categories(selected_categories=self.data.get('categories'))

        page_ids = self.filterable_pages.values_list('id', flat=True)
        self.set_topics(page_ids)
        self.set_authors(page_ids)

    def get_page_set(self):
        query = self.generate_query()
        return self.filterable_pages.filter(query).distinct().order_by(
            '-date_published'
        )

    def first_page_date(self):
        first_post = self.filterable_pages.order_by('date_published').first()
        if first_post:
            return first_post.date_published
        else:
            return date(2010, 1, 1)

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
        if self.errors.get('from_date') or self.errors.get('to_date'):
            return cleaned_data
        else:
            ordered_dates = self.order_from_and_to_date_filters(cleaned_data)
            transformed_dates = self.set_interpreted_date_values(ordered_dates)
            return transformed_dates

    def order_from_and_to_date_filters(self, cleaned_data):
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        # Check if both date_lte and date_gte are present.
        # If the 'start' date is after the 'end' date, swap them.
        if (from_date and to_date) and to_date < from_date:
            data = dict(self.data)
            data_to_date = data['to_date']
            self.cleaned_data['to_date'], data['to_date'] = \
                from_date, data['from_date']
            self.cleaned_data['from_date'], data['from_date'] = \
                to_date, data_to_date
            self.data = data
        return self.cleaned_data

    def set_interpreted_date_values(self, cleaned_data):
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        # If from_ or to_ is filled in, fill them both with sensible values.
        # If neither is filled in, leave them both blank.
        if from_date or to_date:
            if from_date:
                self.data['from_date'] = date.strftime(
                    cleaned_data['from_date'], self.preferred_datetime_format)
            else:
                # If there's a 'to_date' and no 'from_date',
                #  use date of earliest possible filter result as 'from_date'.
                earliest_results = self.first_page_date()
                cleaned_data['from_date'] = earliest_results
                self.data['from_date'] = date.strftime(
                    earliest_results, self.preferred_datetime_format)

            if to_date:
                transformed_to_date = end_of_time_period(
                    self.data['to_date'], cleaned_data['to_date'])
                cleaned_data['to_date'] = transformed_to_date
                self.data['to_date'] = date.strftime(
                    transformed_to_date, self.preferred_datetime_format)
            else:
                # If there's a 'from_date' but no 'to_date', use today's date.
                today = date.today()
                cleaned_data['to_date'] = today
                self.data['to_date'] = date.strftime(
                    today, self.preferred_datetime_format)

        return cleaned_data

    # Sets the html name by replacing the render method to use the given name.
    def set_field_html_name(self, field, new_name):
        """
        This creates wrapper around the normal widget rendering,
        allowing for a custom field name (new_name).
        """
        old_render = field.widget.render
        field.widget.render = lambda name, value, **kwargs: \
            old_render(new_name, value, **kwargs)

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
        fields = ['is_helpful', 'comment', 'language']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['is_helpful'].required = True


class ReferredFeedbackForm(forms.ModelForm):
    """For feedback modules that need to capture the referring page"""
    class Meta:
        model = Feedback
        fields = ['is_helpful', 'referrer', 'comment', 'language']

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
                  'email',
                  'language']

    def __init__(self, *args, **kwargs):
        super(SuggestionFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = True
