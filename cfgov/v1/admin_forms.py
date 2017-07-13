from django import forms


class AkamaiFlushForm(forms.Form):
    url = forms.URLField(required=False,
                         widget=forms.URLInput(attrs={'class': 'url'}))
