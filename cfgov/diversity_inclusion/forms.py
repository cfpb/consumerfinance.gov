from __future__ import division

from django import forms
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


# Form input attributes for Capital Framework compatibility.
# Technique copied from data_research/forms.py
#
# See https://cfpb.github.io/capital-framework/components/cf-forms/
# for documentation on the styles that are being duplicated here.
text_input_attrs = {
    'class': 'a-text-input a-text-input__full',
}


class VoluntaryAssessmentForm(forms.Form):
    institution_name = forms.CharField(
        label='Institution name',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    institution_address = forms.CharField(
        label='Street address',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    institution_city = forms.CharField(
        label='City',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    institution_state = forms.CharField(
        label='State',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    institution_zip = forms.CharField(
        label='ZIP',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    tax_id = forms.CharField(
        label='Tax identification number',
        widget=forms.TextInput(attrs=text_input_attrs),
    )

    contact_name = forms.CharField(
        label='Contact name',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    contact_title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    contact_email = forms.EmailField(
        label='Work email address',
        widget=forms.EmailInput(attrs=text_input_attrs),
    )
    contact_phone = forms.CharField(
        label='Work phone number',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    contact_phone_alt = forms.CharField(
        label='Alternate work phone number',
        required=False,
        widget=forms.TextInput(attrs=text_input_attrs),
    )

    def send_email(self):
        subject = 'Voluntary Diversity Assessment Onboarding Form from ' \
                  + self.cleaned_data['institution_name']
        body = ''

        for (field_name, field) in self.fields.items():
            body += field.label + ': ' + self.cleaned_data[field_name] + '\n'

        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                ['scott.cranfill@cfpb.gov']
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
