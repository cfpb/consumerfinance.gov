from datetime import date
from operator import itemgetter

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import widgets

from wagtail.images.forms import BaseImageForm

from dateutil import parser
from taggit.models import Tag

from v1.models import enforcement_action_page
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
        "%m/%d/%y",  # 10/25/16, 9/1/16
        "%d/%m/%y",  # 13/4/21
        "%m-%d-%y",  # 10-25-16, 9-1-16
        "%d-%m-%y",  # 13-4-21
        "%m/%d/%Y",  # 10/25/2016, 9/1/2016
        "%d/%m/%Y",  # 13/4/2021
        "%m-%d-%Y",  # 10-25-2016, 9-1-2016
        "%d-%m-%Y",  # 13-4-2021
        "%Y-%m-%d",  # 2016-10-25, 2016-9-1
        "%m/%Y",  # 10/2016, 7/2017
        "%m-%Y",  # 10-2016, 7-2017
        "%m/%y",  # 10/16, 4/18
        "%m-%y",  # 10-16, 4-18
        "%Y",  # 2016
    )

    default_widget_attrs = {
        "class": "a-text-input a-text-input--full",
        "type": "date",
        "placeholder": "mm/dd/yyyy",
        "data-type": "date",
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        kwargs.setdefault("input_formats", self.default_input_formats)
        kwargs.setdefault("error_messages", ERROR_MESSAGES["DATE_ERRORS"])

        field_id = kwargs.pop("field_id", None)
        if field_id:
            self.default_widget_attrs["id"] = field_id

        kwargs.setdefault(
            "widget", widgets.DateInput(attrs=self.default_widget_attrs)
        )
        super().__init__(*args, **kwargs)


class FilterableListForm(forms.Form):
    title = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "o-filterable-list-controls_title",
                "class": "a-text-input a-text-input--full",
            }
        ),
    )
    from_date = FilterableDateField(
        field_id="o-filterable-list-controls_from-date"
    )

    to_date = FilterableDateField(
        field_id="o-filterable-list-controls_to-date"
    )

    categories = forms.MultipleChoiceField(
        required=False,
        choices=ref.page_type_choices,
        widget=widgets.SelectMultiple(
            attrs={
                "id": "o-filterable-list-controls_categories",
                "class": "o-multiselect",
                "data-placeholder": "Search for categories",
                "multiple": "multiple",
            }
        ),
    )

    topics = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={
                "id": "o-filterable-list-controls-topics",
                "class": "o-multiselect",
                "data-placeholder": "Search for topics",
                "multiple": "multiple",
            }
        ),
    )

    language = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={
                "id": "o-filterable-list-controls-language",
                "class": "o-multiselect",
                "data-placeholder": "Search for language",
                "multiple": "multiple",
            }
        ),
    )

    preferred_datetime_format = "%Y-%m-%d"

    def __init__(self, *args, **kwargs):
        self.filterable_search = kwargs.pop("filterable_search")

        super().__init__(*args, **kwargs)

        clean_categories(selected_categories=self.data.get("categories"))

        # When the form is created, it needs to make a request to the search
        # backend to be able to populate some of its fields: topics, languages,
        # and the minimum page date.
        self.aggregations = self.filterable_search.get_aggregations()

        self.set_topics()
        self.set_languages()

    def has_unfiltered_results(self):
        return self.aggregations.hits.total.value > 0

    def get_page_set(self):
        self.filterable_search.filter(
            topics=self.cleaned_data.get("topics"),
            categories=self.cleaned_data.get("categories"),
            language=self.cleaned_data.get("language"),
            to_date=self.cleaned_data.get("to_date"),
            from_date=self.cleaned_data.get("from_date"),
        )

        results = self.filterable_search.search(self.cleaned_data.get("title"))

        return results

    def first_page_date(self):
        if not self.has_unfiltered_results():
            return date(2010, 1, 1)

        min_start_date = parser.parse(
            self.aggregations.aggregations.min_start_date.value_as_string
        )

        return min_start_date.date()

    @staticmethod
    def get_filterable_topics(slugs):
        """Given a set of tag slugs, return the list of filterable topics.

        The slugs come from an aggregation over the indexed pages, so this
        only needs to look up the human-readable names for display.
        """
        # tags = Tag.objects.filter(slug__in=slugs).values_list("slug", "name")
        tags = Tag.objects.values_list("slug", "name")

        return tags.distinct().order_by("name")

    def set_topics(self):
        slugs = [
            bucket.key
            for bucket in (self.aggregations.aggregations.topics.buckets)
        ]
        self.fields["topics"].choices = self.get_filterable_topics(slugs)

    # Populate language choices
    def set_languages(self):
        # Get the list of codes in the full set of searchable pages.
        language_aggregation = self.aggregations.aggregations.languages
        language_codes = {b.key for b in language_aggregation.buckets}

        # Grab the language names from the reference list.
        language_options = [
            (code, name)
            for code, name in settings.LANGUAGES
            if code in language_codes
        ]

        # Sort the list of languages by their names.
        self.fields["language"].choices = sorted(
            language_options, key=itemgetter(1)
        )

    def clean(self):
        cleaned_data = super().clean()
        if self.errors.get("from_date") or self.errors.get("to_date"):
            return cleaned_data
        else:
            ordered_dates = self.order_from_and_to_date_filters(cleaned_data)
            transformed_dates = self.set_interpreted_date_values(ordered_dates)
            return transformed_dates

    def order_from_and_to_date_filters(self, cleaned_data):
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")
        # Check if both date_lte and date_gte are present.
        # If the 'start' date is after the 'end' date, swap them.
        if (from_date and to_date) and to_date < from_date:
            data = dict(self.data)
            data_to_date = data["to_date"]
            self.cleaned_data["to_date"], data["to_date"] = (
                from_date,
                data["from_date"],
            )
            self.cleaned_data["from_date"], data["from_date"] = (
                to_date,
                data_to_date,
            )
            self.data = data
        return self.cleaned_data

    def set_interpreted_date_values(self, cleaned_data):
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")
        # If from_ or to_ is filled in, fill them both with sensible values.
        # If neither is filled in, leave them both blank.
        if from_date or to_date:
            if from_date:
                self.data["from_date"] = date.strftime(
                    cleaned_data["from_date"], self.preferred_datetime_format
                )
            else:
                # If there's a 'to_date' and no 'from_date',
                #  use date of earliest possible filter result as 'from_date'.
                earliest_results = self.first_page_date()
                cleaned_data["from_date"] = earliest_results
                self.data["from_date"] = date.strftime(
                    earliest_results, self.preferred_datetime_format
                )

            if to_date:
                transformed_to_date = end_of_time_period(
                    self.data["to_date"], cleaned_data["to_date"]
                )
                cleaned_data["to_date"] = transformed_to_date
                self.data["to_date"] = date.strftime(
                    transformed_to_date, self.preferred_datetime_format
                )
            else:
                # If there's a 'from_date' but no 'to_date', use today's date.
                today = date.today()
                cleaned_data["to_date"] = today
                self.data["to_date"] = date.strftime(
                    today, self.preferred_datetime_format
                )

        return cleaned_data


class EnforcementActionsFilterForm(FilterableListForm):
    statuses = forms.MultipleChoiceField(
        required=False,
        choices=enforcement_action_page.enforcement_statuses,
        widget=widgets.SelectMultiple(
            attrs={
                "id": "o-filterable-list-controls_statuses",
                "class": "o-multiselect",
                "data-placeholder": "Search for statuses",
                "multiple": "multiple",
            }
        ),
    )

    products = forms.MultipleChoiceField(
        required=False,
        choices=enforcement_action_page.enforcement_products,
        widget=widgets.SelectMultiple(
            attrs={
                "id": "o-filterable-list-controls_products",
                "class": "o-multiselect",
                "data-placeholder": "Search for products",
                "multiple": "multiple",
            }
        ),
    )

    def get_page_set(self):
        self.filterable_search.filter(
            topics=self.cleaned_data.get("topics"),
            categories=self.cleaned_data.get("categories"),
            language=self.cleaned_data.get("language"),
            to_date=self.cleaned_data.get("to_date"),
            from_date=self.cleaned_data.get("from_date"),
            statuses=self.cleaned_data.get("statuses"),
            products=self.cleaned_data.get("products"),
        )
        results = self.filterable_search.search(
            title=self.cleaned_data.get("title"),
        )
        return results


class EventArchiveFilterForm(FilterableListForm):
    def get_page_set(self):
        self.filterable_search.filter(
            topics=self.cleaned_data.get("topics"),
            categories=self.cleaned_data.get("categories"),
            language=self.cleaned_data.get("language"),
            to_date=self.cleaned_data.get("to_date"),
            from_date=self.cleaned_data.get("from_date"),
        )
        results = self.filterable_search.search(
            title=self.cleaned_data.get("title")
        )
        return results


class CFGOVImageForm(BaseImageForm):
    """Override the default alt text form widget.

    Our custom image alt text field has no character limit, which renders by
    default as a multi-line textarea field. We instead want to use a
    single-line text input field.
    """

    class Meta(BaseImageForm.Meta):
        widgets = {**BaseImageForm.Meta.widgets, "alt": forms.TextInput}
