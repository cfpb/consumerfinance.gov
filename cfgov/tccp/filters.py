from django import forms

from django_filters import rest_framework as filters


class CardOrderingFilter(filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                "choices": [
                    ("purchase_apr", "Lowest purchase APR"),
                    ("transfer_apr", "Lowest balance transfer APR"),
                    ("low_fees", "Lowest fees"),
                ],
                "initial": "purchase_apr",
            }
        )
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        # If "low_fees" is selected, order first by cards without late fees
        # (boolean), then by first late fee in dollars, in ascending order.
        if value[0] == "low_fees":
            return qs.order_by("late_fees", "late_fee_dollars")

        return super().filter(qs, value)


class CheckboxFilter(filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget", forms.CheckboxInput(attrs={"class": "a-checkbox"})
        )
        super().__init__(*args, **kwargs)


class YesNoFilter(CheckboxFilter):
    def filter(self, qs, value):
        return super().filter(qs, "Yes") if value else qs
