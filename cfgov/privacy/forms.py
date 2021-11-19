from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.core.validators import validate_image_file_extension
from django.http import HttpResponse
from django.template import loader
from django.utils.html import escape


# Form input attributes for Design System compatibility.
# Technique copied from data_research/forms.py
#
# See https://cfpb.github.io/design-system/components/text-inputs
# for documentation on the styles that are being duplicated here.
text_input_attrs = {
    'class': 'a-text-input a-text-input__full',
}
address_attrs = {'class': 'a-text-input'}


class PrivacyActForm(forms.Form):
    # Form fields
    description = forms.CharField(
        label='Description of the record(s) sought',
        widget=forms.Textarea(attrs=text_input_attrs),
    )
    system_of_record = forms.CharField(
        label=('Name of the system of records you believe contain the '
               'record(s)'),
        required=False,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    date_of_records = forms.CharField(
        label='Date of the record(s)',
        help_text=('Or the period in which you believe that the record was '
                   'created'),
        required=False,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    other_info = forms.CharField(
        label='Any additional information',
        help_text=('This may include maiden name, dates of employment, '
                   'account information, etc.'),
        required=False,
        widget=forms.Textarea(attrs=text_input_attrs),
    )
    requestor_name = forms.CharField(
        label='Name of requestor',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    requestor_email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs=text_input_attrs),
    )
    contact_channel = forms.ChoiceField(
        choices=[
            ('email', 'Please send my records via email'),
            ('mail', 'Please send my records by mail'),
        ]
    )
    street_address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs=address_attrs),
    )
    state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs=address_attrs),
    )
    zip_code = forms.CharField(
        label='Zip',
        required=False,
        widget=forms.TextInput(attrs=address_attrs),
    )
    supporting_documentation = forms.FileField(
        required=False,
        validators=[validate_image_file_extension],
    )
    full_name = forms.CharField(
        label='Full name',
        widget=forms.TextInput(attrs=text_input_attrs),
    )

    # Form validations
    def escaped_fields(self):
        data = {}
        for (key, value) in self.cleaned_data.items():
            data.update({key: escape(value)})
        return data

    def require_address_if_mailing(self):
        data = self.cleaned_data
        msg = "Mailing address is required if requesting records by mail."
        if data['contact_channel'] == 'mail':
            if not (data['street_address'] and data['city'] and data['state']
                    and data['zip_code']):
                self.add_error('street_address', forms.ValidationError(msg))

    def combined_file_size(self, files):
        total = 0
        for f in files:
            total += f.size
        return total

    def limit_file_size(self, files):
        mb = 1048576  # one megabyte in bytes
        max_bytes = mb * 6  # 6 MB
        total_uploaded_bytes = self.combined_file_size(files)
        if total_uploaded_bytes > max_bytes:
            display_size = round(total_uploaded_bytes / mb, 1)
            err = forms.ValidationError(
                f"Total size of uploaded files ({display_size} MB) was "
                "greater than size limit (2 MB)."
            )
            self.add_error('supporting_documentation', err)

    def limit_number_of_files(self, files):
        max_files = 6
        if len(files) > max_files:
            err = forms.ValidationError(
                f"Please choose {max_files} or fewer files. "
                f"You chose {len(files)}."
            )
            self.add_error('supporting_documentation', err)

    def clean(self):
        super().clean()
        self.require_address_if_mailing()
        self.uploaded_files = self.files.getlist('supporting_documentation')
        self.limit_file_size(self.uploaded_files)
        self.limit_number_of_files(self.uploaded_files)
        return self.escaped_fields()

    # Email message
    def email_body(self):
        data = self.cleaned_data
        data.update({
            'num_files': len(self.uploaded_files),
            'uploaded_files': self.uploaded_files,
        })
        return loader.render_to_string(self.email_template, data)

    def format_subject(self):
        name = self.cleaned_data['requestor_name']
        truncated_name = (name[:20] + '...') if len(name) > 24 else name
        return self.email_subject + truncated_name

    def send_email(self):
        email = EmailMessage(
            subject=self.format_subject(),
            body=self.email_body(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.PRIVACY_EMAIL_TARGET],
            reply_to=[self.cleaned_data['requestor_email']],
        )
        email.content_subtype = 'html'

        for f in self.uploaded_files:
            email.attach(f.name, f.read(), f.content_type)

        try:
            email.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')


class DisclosureConsentForm(PrivacyActForm):
    # Additional fields beyond what's defined in PrivacyActForm
    consent_text = '''\
        I declare under penalty of perjury under the laws of the United States
        of America that the foregoing is true and correct, and that I am the
        person named above and consenting to and authorizing disclosure of my
        records, or records that I am entitled to request as the parent of a
        minor or the legal guardian of an incompetent, and I understand that
        any falsification of this statement is punishable under the provisions
        of 18 U.S.C. § 1001 by a fine, imprisonment of not more than five
        years, or both, and that requesting or obtaining any record(s) under
        false pretenses is punishable under the provisions of 5 U.S.C.
        § 552a(i)(3) by a fine of not more than $5,000.
        '''
    consent = forms.BooleanField(
        label=consent_text,
        widget=forms.CheckboxInput(attrs={'class': 'a-checkbox'}),
    )
    recipient_name = forms.CharField(
        label='Name of recipient',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    recipient_email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs=text_input_attrs),
    )

    email_subject = 'Disclosure request from consumerfinance.gov: '

    email_template = 'privacy/disclosure_consent_email.html'


class RecordsAccessForm(PrivacyActForm):
    # Additional fields beyond what's defined in PrivacyActForm
    consent_text = '''\
        I declare under penalty of perjury under the laws of the United
        States of America that the foregoing is true and correct, and that I
        am the person named above and requesting access to my records, or
        records that I am entitled to request as the parent of a minor or the
        legal guardian of an incompetent, and I understand that any
        falsification of this statement is punishable under the provisions
        of 18 U.S.C. § 1001 by a fine, imprisonment of not more than five
        years, or both, and that requesting or obtaining any record(s) under
        false pretenses is punishable under the provisions of 5 U.S.C.
        § 552a(i)(3) by a fine of not more than $5,000.
        '''
    consent = forms.BooleanField(
        label=consent_text,
        widget=forms.CheckboxInput(attrs={'class': 'a-checkbox'}),
    )
    email_subject = 'Records request from consumerfinance.gov: '

    email_template = 'privacy/records_access_email.html'
