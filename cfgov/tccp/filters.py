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
        if value[0].endswith("_apr"):
            # If we're sorting by an APR, we want to exclude any cards that
            # don't specify that APR.
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
