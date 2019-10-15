from __future__ import division

from django import forms
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

# Is there a way to use this to define the fields on the forms,
# if field tpe and widget type and required status were added to the tuples?
fields = [
    ('institution_name', 'Institution name'),
    ('institution_address', 'Street address'),
    ('institution_city', 'City'),
    ('institution_state', 'State'),
    ('institution_zip', 'ZIP'),
    ('tax_id', 'Tax identification number'),
    ('contact_name', 'Contact name'),
    ('contact_title', 'Title'),
    ('contact_email', 'Work email address'),
    ('contact_phone', 'Work phone number'),
    ('contact_phone_alt', 'Alternate work phone number'),
]


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
        from_email = self.cleaned_data['contact_email']
        subject = 'Voluntary Diversity Assessment Onboarding Form from ' \
                  + self.cleaned_data['institution_name']

        body = ''
        for (field, label) in fields:
            body += label + ': ' + self.cleaned_data[field] + '\n'

        try:
            send_mail(subject, body, from_email, ['scott.cranfill@cfpb.gov'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
