from django import forms

from .enums import CreditTierChoices, StateChoices
from .situations import SituationChoices, get_situation_by_title
from .widgets import Select, SituationSelectMultiple


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
        widget=Select(
            attrs={
                "aria-describedby": "location-required",
                "data-js-hook": "behavior_select-location",
            }
        ),
    )
    situations = forms.TypedMultipleChoiceField(
        choices=SituationChoices,
        coerce=get_situation_by_title,
        widget=SituationSelectMultiple(),
        required=False,
    )
