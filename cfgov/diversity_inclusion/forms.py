from __future__ import division

from django import forms


# Form input attributes for Capital Framework compatibility.
# Technique copied from data_research/forms.py
#
# See https://cfpb.github.io/capital-framework/components/cf-forms/
# for documentation on the styles that are being duplicated here.
text_input_attrs = {
    'class': 'a-text-input a-text-input__full',
}

# This is needed to disable Django's default Textarea sizing.
textarea_attrs = {
    'rows': None,
    'cols': None,
}
textarea_attrs.update(text_input_attrs)


class VoluntaryAssessmentForm(forms.Form):
    institution_name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    institution_address = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    institution_city = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    institution_state = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    institution_zip = forms.CharField(
        label='Institution ZIP Code',
        max_length=10,
        widget=forms.TextInput(attrs=text_input_attrs),
    )

    lei = forms.CharField(
        label='LEI',
        required=False,
        max_length=32,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    rssd_id = forms.CharField(
        label='RSSD ID',
        required=False,
        max_length=32,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    tax_id = forms.CharField(
        label='Tax ID Number (TIN)',
        required=False,
        max_length=32,
        widget=forms.TextInput(attrs=text_input_attrs),
    )

    contact_name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    contact_title = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    contact_email = forms.EmailField(
        max_length=250,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    contact_phone = forms.CharField(
        max_length=24,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    contact_phone_alt = forms.CharField(
        label='Alternate contact phone (optional)',
        required=False,
        max_length=24,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
