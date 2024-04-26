from django import forms

from search.elasticsearch_helpers import make_safe


class SearchForm(forms.Form):
    q = forms.CharField(required=False, strip=True)

    partial = forms.BooleanField(required=False)

    page = forms.IntegerField(required=False, min_value=1, max_value=14)

    grade_level = forms.MultipleChoiceField(
        required=False,
        choices=(
            ("1", "9-10"),
            ("2", "11-12"),
            ("3", "6-8"),
            ("4", "k-1"),
            ("5", "2-3"),
            ("6", "4-5"),
        ),
    )

    activity_duration = forms.MultipleChoiceField(
        required=False,
        choices=(
            ("1", "15-20"),
            ("2", "45-60"),
            ("3", "75-90"),
        ),
    )

    topic = forms.MultipleChoiceField(
        required=False,
        choices=(
            ("2", "making-money"),
            ("3", "increasing-earnings"),
            ("4", "getting-paid"),
            ("5", "paying-taxes"),
            ("7", "choosing-how-to-save"),
            ("8", "building-emergency-savings"),
            ("9", "saving-for-college"),
            ("10", "saving-for-long-term-goals"),
            ("11", "saving-for-short-term-goals"),
            ("12", "investing"),
            ("14", "managing-risk"),
            ("15", "preventing-fraud-and-identity-theft"),
            ("17", "budgeting"),
            ("18", "buying-things"),
            ("19", "paying-bills"),
            ("20", "paying-for-college"),
            ("22", "getting-loans"),
            ("23", "managing-credit"),
            ("24", "giving-to-others"),
            ("25", "becoming-an-entrepreneur"),
            ("26", "learning-about-careers"),
            ("27", "banking-options"),
            ("29", "using-insurance"),
        ),
    )

    def clean_q(self):
        return make_safe(self.cleaned_data["q"])

    def clean_page(self):
        return self.cleaned_data["page"] or 1
