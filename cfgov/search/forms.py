from django import forms


class ExternalLinksForm(forms.Form):
    url = forms.CharField()
