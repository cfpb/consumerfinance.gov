from django import forms

from django_filters import rest_framework as filters


class CardOrderingFilter(filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                "choices": [
                    ("purchase_apr", "Lowest purchase APR"),
                    ("transfer_apr", "Lowest balance transfer APR"),
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
            ordering = ["purchase_apr_for_tier"]
        elif value[0] == "transfer_apr":
            # If we're sorting by transfer APR, we want to exclude cards that
            # don't have either a tier-specific APR or a {minimum, maximum}
            # range, which we previously coalesced into the
            # transfer_apr_for_ordering field.
            qs = qs.exclude(transfer_apr_for_ordering__isnull=True)

            # We then order by that column first and purchase APR second.
            ordering = ["transfer_apr_for_ordering", "purchase_apr_for_tier"]

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
