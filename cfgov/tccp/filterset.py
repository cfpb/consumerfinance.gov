from django_filters import rest_framework as filters

from .enums import CreditTierChoices, StateChoices
from .filters import CheckboxFilter, OrderingFilter, YesNoFilter
from .models import CardSurveyData
from .widgets import Select


class CardSurveyDataFilterSet(filters.FilterSet):
    targeted_credit_tiers = filters.ChoiceFilter(
        choices=CreditTierChoices[1:],
        lookup_expr="contains",
        label="Your credit score",
        initial=CreditTierChoices[2][0],
        null_label=None,
        empty_label=None,
        widget=Select,
    )
    geo_availability = filters.ChoiceFilter(
        choices=StateChoices,
        method="filter_geo_availability",
        label="Availability",
        null_label="Available everywhere in the US",
        empty_label="Show me cards regardless of where they are available",
        widget=Select,
    )
    no_balance_transfer_fees = YesNoFilter(
        "balance_transfer_fees", label="No balance transfer fees", exclude=True
    )
    introductory_apr_offered = YesNoFilter(label="Introductory APR offers")
    secured_card = YesNoFilter(label="Secured card")
    no_periodic_fees = CheckboxFilter(
        "periodic_fee_type",
        method="filter_for_empty_list",
        label="No periodic fees",
        exclude=True,
    )
    rewards = YesNoFilter(label="Offers rewards")
    ordering = OrderingFilter(
        choices=[
            ("purchase_apr", "Lowest purchase APR"),
            ("transfer_apr", "Lowest balance transfer APR"),
            ("late_fee_dollars", "Lowest first late fee"),
        ],
        label="Sort by",
        initial="purchase_apr",
        null_label=None,
        empty_label=None,
        widget=Select,
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

    def filter_geo_availability(self, queryset, name, value):
        return queryset.available_in(value)

    def filter_for_empty_list(self, queryset, name, value):
        return queryset.filter(**{name: []}) if value else queryset
