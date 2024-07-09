from functools import reduce
from operator import or_

from django import forms
from django.db.models import Q

from django_filters import rest_framework as filters

from .enums import CreditTierChoices, RewardsChoices, StateChoices
from .filters import CardOrderingFilter, CheckboxFilter, MultipleCheckboxFilter
from .models import CardSurveyData
from .situations import SituationChoices, get_situation_by_title
from .widgets import OrderingSelect, Select


class CardSurveyDataFilterSet(filters.FilterSet):
    credit_tier = filters.ChoiceFilter(
        choices=CreditTierChoices[1:],
        method="filter_credit_tier",
        label="Your credit score",
        initial=CreditTierChoices[2][0],
        null_label=None,
        empty_label=None,
        widget=Select,
    )
    location = filters.ChoiceFilter(
        choices=StateChoices,
        method="filter_location",
        label="Available in location",
        empty_label="Everywhere",
        widget=Select,
    )
    situations = filters.TypedMultipleChoiceFilter(
        choices=SituationChoices,
        coerce=get_situation_by_title,
        method="filter_noop",
        widget=forms.MultipleHiddenInput,
    )
    small_institution = CheckboxFilter(
        "issued_by_top_25_institution", label="Small institution", exclude=True
    )
    no_account_fee = CheckboxFilter(
        "periodic_fee_type",
        method="filter_for_empty_list",
        label="No account fee",
    )
    rewards = MultipleCheckboxFilter(
        choices=RewardsChoices,
        label="Offers rewards",
        method="filter_for_contains",
    )
    ordering = CardOrderingFilter(
        label="Sort by",
        null_label=None,
        empty_label=None,
        widget=OrderingSelect,
    )

    class Meta:
        model = CardSurveyData
        fields = []

    def __init__(self, data=None, *args, **kwargs):
        # Set field defaults to their initial values, if not set.
        #
        # https://django-filter.readthedocs.io/en/stable/guide/tips.html#using-initial-values-as-defaults
        #
        # We prevent data from being None because we always want at
        # least some filtering to occur, for example the ordering.
        data = data.copy() if data else {}

        for name, f in self.base_filters.items():
            initial = f.extra.get("initial")

            if not data.get(name) and initial:
                data[name] = initial

        super().__init__(data, *args, **kwargs)

    def filter_credit_tier(self, queryset, name, value):
        return queryset.for_credit_tier(value)

    def filter_location(self, queryset, name, value):
        return queryset.available_in(value)

    def filter_for_empty_list(self, queryset, name, value):
        return queryset.filter(**{name: []}) if value else queryset

    def filter_for_contains(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                reduce(
                    or_,
                    [
                        Q(**{f"{name}__contains": subvalue})
                        for subvalue in value
                    ],
                )
            )

        return queryset

    def filter_noop(self, queryset, name, value):
        return queryset
