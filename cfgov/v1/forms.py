from collections import Counter
from datetime import date

from django import forms
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.forms import widgets

from taggit.models import Tag

from v1.models import enforcement_action_page
from v1.models.feedback import Feedback
from v1.util import ERROR_MESSAGES, ref
from v1.util.categories import clean_categories
from v1.util.datetimes import end_of_time_period


class FilterableDateField(forms.DateField):
    def validate_after_1900(date):
        strftime_earliest_year = 1900
        if date.year < strftime_earliest_year:
            raise ValidationError("Please enter a date of 1/1/1900 or later.")

    default_validators = [validate_after_1900]

    default_input_formats = (
        '%m/%d/%y',     # 10/25/16, 9/1/16
        '%d/%m/%y',     # 13/4/21
        '%m-%d-%y',     # 10-25-16, 9-1-16
        '%d-%m-%y',     # 13-4-21
        '%m/%d/%Y',     # 10/25/2016, 9/1/2016
        '%d/%m/%Y',     # 13/4/2021
        '%m-%d-%Y',     # 10-25-2016, 9-1-2016
        '%d-%m-%Y',     # 13-4-2021
        '%Y-%m-%d',     # 2016-10-25, 2016-9-1
        '%m/%Y',        # 10/2016, 7/2017
        '%m-%Y',        # 10-2016, 7-2017
        '%m/%y',        # 10/16, 4/18
        '%m-%y',        # 10-16, 4-18
        '%Y',           # 2016
    )

    default_widget_attrs = {
        'class': 'a-text-input a-text-input__full',
        'type': 'date',
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
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_categories',
            'class': 'o-multiselect',
            'data-placeholder': 'Search for categories',
            'multiple': 'multiple',
        })
    )

    topics = forms.MultipleChoiceField(
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

    archived = forms.ChoiceField(
        choices=[
            ('include', 'Show all items (default)'),
            ('exclude', 'Exclude archived items'),
            ('only', 'Show only archived items'),
        ]
    )

    preferred_datetime_format = '%Y-%m-%d'

    def __init__(self, *args, **kwargs):
        self.filterable_search = kwargs.pop('filterable_search')
        self.wagtail_block = kwargs.pop('wagtail_block')
        self.filterable_categories = kwargs.pop('filterable_categories')

        # This cache key is used for caching authors, topics, page_ids, and
        # the full set of Elasticsearch results for this form used to generate
        # them.
        # Default the cache key prefix to this form's hash if it's not
        # provided.
        self.cache_key_prefix = kwargs.pop('cache_key_prefix', hash(self))

        super(FilterableListForm, self).__init__(*args, **kwargs)

        clean_categories(selected_categories=self.data.get('categories'))

        self.all_filterable_results = self.get_all_filterable_results()
        page_ids = self.get_all_page_ids()
        self.set_topics(page_ids)
        self.set_authors(page_ids)

    def get_all_filterable_results(self):
        """ Get all filterable document results from Elasticsearch

        This set of results is used to populate the list of all page_ids,
        below, which is in turn used for populating topics and authors
        relevant to those pages.

        This first document in this result set is also used to determine the
        earliest post date, also below, when a to_date is given but
        from_date is not.
        """
        # Cache the full list of filterable results. This avoids having to
        # generate the same list with every request. When a filterable page is
        # is saved, the cache key for this fix prefix will be deleted.
        all_filterable_results = cache.get(
            f"{self.cache_key_prefix}-all_filterable_results"
        )
        if all_filterable_results is None:
            all_filterable_results = self.filterable_search.get_raw_results()
            cache.set(
                f"{self.cache_key_prefix}-all_filterable_results",
                all_filterable_results,
            )
        return all_filterable_results

    def get_all_page_ids(self):
        """ Return a list of all possible filterable page ids """
        page_ids = cache.get(f"{self.cache_key_prefix}-page_ids")
        if page_ids is None:
            page_ids = [
                result.meta.id for result in self.all_filterable_results
            ]
            cache.set(f"{self.cache_key_prefix}-page_ids", page_ids)
        return page_ids

    def get_categories(self):
        categories = self.cleaned_data.get('categories')

        # If no categories are submitted by the form
        if categories == []:
            # And we have defined a prexisting set of categories
            # to limit results by Using CategoryFilterableMixin
            if self.filterable_categories not in ([], None):
                return ref.get_category_children(
                    self.filterable_categories)
        return categories

    def get_order_by(self):
        if self.wagtail_block is not None:
            return self.wagtail_block.value.get('order_by', '-date_published')
        else:
            return '-date_published'

    def get_page_set(self):
        categories = self.get_categories()

        self.filterable_search.filter(
            topics=self.cleaned_data.get('topics'),
            categories=categories,
            authors=self.cleaned_data.get('authors'),
            to_date=self.cleaned_data.get('to_date'),
            from_date=self.cleaned_data.get('from_date'),
            archived=self.cleaned_data.get('archived'),
        )

        results = self.filterable_search.search(
            title=self.cleaned_data.get('title'),
            order_by=self.get_order_by()
        )

        return results

    def first_page_date(self):
        if len(self.all_filterable_results) > 0:
            first_post = self.all_filterable_results[0]
            return first_post.date_published.date()
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
        if self.wagtail_block:
            # Cache the topics for this filterable list form to avoid
            # repeated database lookups of the same data.
            topics = cache.get(f"{self.cache_key_prefix}-topics")
            if topics is None:
                topics = self.wagtail_block.block.get_filterable_topics(
                    page_ids,
                    self.wagtail_block.value
                )
                cache.set(f"{self.cache_key_prefix}-topics", topics)

            self.fields['topics'].choices = topics

    # Populate Authors' choices
    def set_authors(self, page_ids):
        # Cache the authors for this filterable list form to avoid
        # repeated database lookups of the same data.
        options = cache.get(f"{self.cache_key_prefix}-authors")
        if options is None:
            authors = Tag.objects.filter(
                v1_cfgovauthoredpages_items__content_object__id__in=page_ids
            ).values_list('slug', 'name')
            options = self.prepare_options(arr=authors)
            cache.set(f"{self.cache_key_prefix}-authors", options)
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

    def clean_archived(self):
        data = self.cleaned_data['archived']
        if data == 'exclude':
            return ['no', 'never']
        elif data == 'only':
            return ['yes']

        return None


class EnforcementActionsFilterForm(FilterableListForm):

    statuses = forms.MultipleChoiceField(
        required=False,
        choices=enforcement_action_page.enforcement_statuses,
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_statuses',
            'class': 'o-multiselect',
            'data-placeholder': 'Search for statuses',
            'multiple': 'multiple',
        })
    )

    products = forms.MultipleChoiceField(
        required=False,
        choices=enforcement_action_page.enforcement_products,
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_products',
            'class': 'o-multiselect',
            'data-placeholder': 'Search for products',
            'multiple': 'multiple',
        })
    )

    def get_page_set(self):
        self.filterable_search.filter(
            topics=self.cleaned_data.get('topics'),
            categories=self.cleaned_data.get('categories'),
            authors=self.cleaned_data.get('authors'),
            to_date=self.cleaned_data.get('to_date'),
            from_date=self.cleaned_data.get('from_date'),
            statuses=self.cleaned_data.get('statuses'),
            products=self.cleaned_data.get('products')
        )
        results = self.filterable_search.search(
            title=self.cleaned_data.get('title'),
        )
        return results


class EventArchiveFilterForm(FilterableListForm):

    def get_page_set(self):
        self.filterable_search.filter(
            topics=self.cleaned_data.get('topics'),
            categories=self.cleaned_data.get('categories'),
            authors=self.cleaned_data.get('authors'),
            to_date=self.cleaned_data.get('to_date'),
            from_date=self.cleaned_data.get('from_date'),
        )
        results = self.filterable_search.search(
            title=self.cleaned_data.get('title'),
            order_by=self.get_order_by()
        )
        return results


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
