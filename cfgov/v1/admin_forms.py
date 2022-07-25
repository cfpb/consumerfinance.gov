from django import forms


class CacheInvalidationForm(forms.Form):
    url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "url"})
    )
