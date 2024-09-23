from django import forms


class ImportForm(forms.Form):
    page_file = forms.FileField(label="Page file", required=True)
