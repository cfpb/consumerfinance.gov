from django import forms

import django_filters
from django_filters import rest_framework as filters

from .enums import CreditTierChoices


class OrderingFilter(django_filters.OrderingFilter):
    def filter(self, qs, value):
        # If the user didn't specify an ordering,
        # we default to the first one in the list.
        value = value or [self.extra["choices"][0][0]]

        if "apr" in value[0]:
            # value contains the name of the APR field we want to sort by, for
            # example ["purchase_apr"].
            #
            # This doesn't actually refer to a field on the model. We want to
            # instead sort by the model field specific to the credit tier that we
            # are also filtering on.
            #
            # For example, when sorting by purchase_apr for all credit tiers, we
            # want to use purchase_apr_minimum. When sorting by purchase_apr for
            # the poor credit tier, we want to use purchase_apr_poor.
            value = [self.get_field_for_tier(value[0])]

        return super().filter(qs, value)

    def get_field_for_tier(self, field):
        tier = self.parent.form.cleaned_data["targeted_credit_tiers"]

        tier_column_suffix = {
            CreditTierChoices[1][0]: "poor",
            CreditTierChoices[2][0]: "good",
            CreditTierChoices[3][0]: "great",
        }[tier]

        return f"{field}_{tier_column_suffix}"


class CheckboxFilter(filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget", forms.CheckboxInput(attrs={"class": "a-checkbox"})
        )
        super().__init__(*args, **kwargs)


class YesNoFilter(CheckboxFilter):
    def filter(self, qs, value):
        return super().filter(qs, "Yes") if value else qs
