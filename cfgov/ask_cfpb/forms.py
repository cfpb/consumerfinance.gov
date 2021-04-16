from django import forms
from django.core.validators import RegexValidator

from ask_cfpb.models.search import make_safe


legacy_facet_validator = RegexValidator(
    regex=r'(?:category|audience|tag)_exact:\S+',
    message='Not a valid legacy facet',
)


class AutocompleteForm(forms.Form):
    term = forms.CharField(strip=True)

    def clean_term(self):
        return make_safe(self.cleaned_data['term'])


class SearchForm(forms.Form):
    q = forms.CharField(strip=True)
    correct = forms.BooleanField(required=False, initial=True)

    def clean_q(self):
        return make_safe(self.cleaned_data['q'])

    def clean_correct(self):
        if 'correct' not in self.data:
            return self.fields['correct'].initial
        if self.data['correct'] == '0':
            self.cleaned_data['correct'] = False
        return self.cleaned_data['correct']
