from django import forms

from .enums import CreditTierChoices, StateChoices
from .situations import SituationChoices, get_situation_by_title
from .widgets import LandingPageRadioSelect, Select


class LandingPageForm(forms.Form):
    credit_tier = forms.ChoiceField(
        choices=CreditTierChoices[1:],
        initial=CreditTierChoices[2],
        label="Your credit score range",
        widget=Select(),
    )
    location = forms.ChoiceField(
        choices=[("", "Select your location")] + StateChoices,
        label="Your location",
        widget=Select(),
    )
    situation = forms.TypedChoiceField(
        choices=SituationChoices,
        coerce=get_situation_by_title,
        widget=LandingPageRadioSelect(),
    )
