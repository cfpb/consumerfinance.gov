from django import forms

from django_filters import rest_framework as filters

from .widgets import CheckboxSelectMultiple


class CardOrderingFilter(filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                "choices": [
                    ("purchase_apr", "Purchase APR"),
                    ("transfer_apr", "Balance transfer APR"),
                    ("product_name", "Card name"),
                ],
                "initial": "purchase_apr",
            }
        )
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        ordering = []

        if value[0] == "purchase_apr":
            # If we're sorting by purchase APR, we sort by the tier-specific
            # purchase APR that we previously annotated.
            ordering = ["purchase_apr_for_tier_max"]
        elif value[0] == "transfer_apr":
            # If we're sorting by transfer APR, we want to exclude cards that
            # don't have either a tier-specific APR or a {minimum, maximum}
            # range, which we previously coalesced into the
            # transfer_apr_for_tier_max field.
            qs = qs.exclude(transfer_apr_for_tier_max__isnull=True)

            # We then order by that column first and purchase APR second.
            ordering = [
                "transfer_apr_for_tier_max",
                "purchase_apr_for_tier_max",
            ]

        # We always specify product name as the fallback ordering.
        return super().filter(qs, ordering + ["product_name"])


class CheckboxFilter(filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget", forms.CheckboxInput(attrs={"class": "a-checkbox"})
        )
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        return super().filter(qs, True) if value else qs


class MultipleCheckboxFilter(filters.MultipleChoiceFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget",
            CheckboxSelectMultiple(),
        )
        super().__init__(*args, **kwargs)
