from django import forms
from django.db.models import F, Q

from django_filters import rest_framework as filters


class CardOrderingFilter(filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                "choices": [
                    ("purchase_apr", "Lowest purchase APR"),
                    ("transfer_apr", "Lowest balance transfer APR"),
                    ("low_fees", "Lowest first late fee"),
                ],
                "initial": "purchase_apr",
            }
        )
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        # If "low_fees" is selected, order first by cards without late fees
        # (boolean), then by first late fee in dollars, in ascending order.
        # We want to treat an empty first late fee as zero on the frontend,
        # so we sort them first.
        if value[0] == "low_fees":
            qs = qs.order_by(
                "late_fees", F("late_fee_dollars").asc(nulls_first=True)
            )

            # If we're sorting by low fees, we also want to filter out cards
            # that have late fees (late_fees=True) but don't specify a first
            # late fee in dollars (late_fee_dollars=None).
            return qs.exclude(
                Q(late_fees=True) & Q(late_fee_dollars__isnull=True)
            )

        # Otherwise, if we're sorting by an APR, we want to exclude any cards
        # that don't specify that APR.
        qs = qs.exclude(**{f"{value[0]}__isnull": True})

        return super().filter(qs, value)


class CheckboxFilter(filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget", forms.CheckboxInput(attrs={"class": "a-checkbox"})
        )
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        return super().filter(qs, True) if value else qs
