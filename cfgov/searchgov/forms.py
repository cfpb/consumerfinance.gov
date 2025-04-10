from django import forms

from core.utils import make_safe


class SearchForm(forms.Form):
    q = forms.CharField(strip=True)
    page = forms.IntegerField(required=False)

    def clean_q(self):
        return make_safe(self.cleaned_data["q"])

    def clean_page(self):
        raw = self.cleaned_data["page"]
        if raw is None:
            return 1
        try:
            return int(raw)
        except ValueError:
            return 1
