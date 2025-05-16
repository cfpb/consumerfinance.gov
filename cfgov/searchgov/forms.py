from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(strip=True)
    page = forms.IntegerField(required=False)

    def clean_q(self):
        return self.cleaned_data["q"].strip()

    def clean_page(self):
        raw = self.cleaned_data["page"]
        if raw is None:
            return 1
        try:
            return int(raw)
        except ValueError:
            return 1
