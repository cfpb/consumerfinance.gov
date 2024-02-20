from django import forms

from .enums import CreditTierChoices
from .situations import SituationChoices, get_situation_by_title
from .widgets import LandingPageRadioSelect, Select


class LandingPageForm(forms.Form):
    credit_tier = forms.ChoiceField(
        choices=CreditTierChoices[1:],
        initial=CreditTierChoices[2],
        label="Your credit score",
        widget=Select(),
    )

    situation = forms.TypedChoiceField(
        choices=SituationChoices,
        coerce=get_situation_by_title,
        widget=LandingPageRadioSelect(),
    )
