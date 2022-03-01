from django import forms
from django.forms import widgets

from hmda.resources.hmda_data_options import (
    HMDA_FIELD_DESC_OPTIONS,
    HMDA_GEO_OPTIONS,
    HMDA_RECORDS_OPTIONS,
)


class HmdaFilterableForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    geo = forms.ChoiceField(
        required=False, choices=HMDA_GEO_OPTIONS, widget=widgets.Select()
    )
    records = forms.ChoiceField(
        required=False,
        choices=HMDA_RECORDS_OPTIONS,
        widget=widgets.RadioSelect(),
    )
    field_descriptions = forms.ChoiceField(
        required=False,
        choices=HMDA_FIELD_DESC_OPTIONS,
        widget=widgets.RadioSelect(),
    )
