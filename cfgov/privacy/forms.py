from textwrap import dedent

from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.template import loader
from django.core.validators import validate_image_file_extension
from django.http import HttpResponse


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
        label='Name of the system of records you believe contain the record(s)',
        required=False,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    date_of_records = forms.CharField(
        label='Date of the record(s)',
        help_text='Or the period in which you believe that the record was created',  # noqa: E501
        required=False,
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    other_info = forms.CharField(
        label='Any additional information',
        help_text='This may include maiden name, dates of employment, account information, etc.',  # noqa: E501
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
        widget=forms.RadioSelect,
        choices=[
            ('email', 'Please send my records by email'),
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
    def require_address_if_mailing(self):
        data = self.cleaned_data
        if data['contact_channel'] == 'mail':
            if not (data['street_address'] and data['city'] and data['state']
                    and data['zip_code']):
                msg = "Mailing address is required if requesting records by mail."  # noqa: E501
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
            err = forms.ValidationError(f"Total size of uploaded files ({display_size} MB) was greater than size limit (2 MB).")  # noqa: E501
            self.add_error('supporting_documentation', err)

    def limit_number_of_files(self, files):
        max_files = 6
        if len(files) > max_files:
            err = forms.ValidationError(f"Please choose {max_files} or fewer files. You chose {len(files)}.")  # noqa: E501
            self.add_error('supporting_documentation', err)

    def clean(self):
        super().clean()
        self.require_address_if_mailing()
        uploaded_files = self.files.getlist('supporting_documentation')
        self.limit_file_size(uploaded_files)
        self.limit_number_of_files(uploaded_files)

    # Email message
    def format_contact_info(self, data):
        contact_info = f"Please send my records by {data['contact_channel']}."
        if data['contact_channel'] == 'mail':
            contact_info += f'''
            Recipient mailing address:
            {data['street_address']}
            {data['city']}, {data['state']} {data['zip_code']}
            '''
        return contact_info

    def format_files(self):
        uploaded_files = self.files.getlist('supporting_documentation')
        files = f'{len(uploaded_files)} files attached.'
        for f in uploaded_files:
            files += '\n        - ' + f.name
        return files

    def send_email(self):
        data = self.cleaned_data
        uploaded_files = self.files.getlist('supporting_documentation')
        data.update({'uploaded_files': uploaded_files})
        subject = self.format_subject(data['requestor_name'])
        from_email = settings.DEFAULT_FROM_EMAIL
        # recipient_list = ['FOIA@consumerfinance.gov']
        recipient_list = ['elizabeth.lorton@cfpb.gov']

        body = self.email_body(data)

        email = EmailMessage(
            subject,
            body,
            from_email,
            recipient_list,
            reply_to=[data['requestor_email']]
        )
        email.content_subtype = 'html'

        for f in uploaded_files:
            email.attach(f.name, f.read(), f.content_type)

        try:
            email.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')


class DisclosureConsentForm(PrivacyActForm):
    consent_text = '''
        I declare under penalty of perjury under the laws
        of the United States of America that the foregoing is true and
        correct, and that I am the person named above and consenting
        to and authorizing disclosure of my records [or records
        that I am entitled to request as the parent of a minor or
        the legal guardian of an incompetent], and I understand that
        any falsification of this statement is punishable under the
        provisions of 18 U.S.C. § 1001 by a fine, imprisonment of
        not more than five years, or both, and that requesting or
        obtaining any record(s) under false pretenses is punishable
        under the provisions of 5 U.S.C. § 552a(i)(3) by a fine of not
        more than $5,000.'''
    consent = forms.BooleanField(
        label=consent_text,
        widget=forms.CheckboxInput(attrs={'class': 'a-checkbox'}),
    )
    # Inherit most form fields from the PrivacyActForm class
    recipient_name = forms.CharField(
        label='Name of recipient',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    recipient_email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs=text_input_attrs),
    )

    def format_subject(self, name):
        return f'Disclosure request from consumerfinance.gov: {name}'

    def email_body(self, data):
        return dedent(f'''
        The following information was submitted via web form on consumerfinance.gov/privacy/disclosure-consent. Any attachments have not been scanned for viruses and may be unsafe.

        Consent for disclosure of records protected under the Privacy Act
        =================================================================

        # Information about the request
        Description of the nature of the records sought: {data['description']}
        Name of the system of records that you believe contain the record requested: {data['system_of_record']}
        Date of the record(s): {data['date_of_records']}
        Any other information that might assist the CFPB in identifying the record sought: {data['other_info']}

        # Contact Information
        Name of requestor: {data['requestor_name']}
        Requestor email address: {data['requestor_email']}
        Name of recipient: {data['recipient_name']}
        Recipient email address: {data['recipient_email']}
        {self.format_contact_info(data)}

        Supporting documentation: {self.format_files()}

        # Consent for disclosure of records
        Full name: {data['full_name']}
        {self.consent_text}: {data['consent']}
        ''')


class RecordsAccessForm(PrivacyActForm):
    # Inherit form fields from the PrivacyActForm class
    consent_text = '''
        I declare under penalty of perjury under the laws of the United
        States of America that the foregoing is true and correct, and that
        I am the person named above and requesting access to my records
        [or records that I am entitled to request as the parent of a minor
        or the legal guardian of an incompetent], and I understand that
        any falsification of this statement is punishable under the
        provisions of 18 U.S.C. § 1001 by a fine, imprisonment of not
        more than five years, or both, and that requesting or obtaining
        any record(s) under false pretenses is punishable under the
        provisions of 5 U.S.C. § 552a(i)(3) by a fine of not more than
        $5,000.'''
    consent = forms.BooleanField(
        label=consent_text,
        widget=forms.CheckboxInput(attrs={'class': 'a-checkbox'}),
    )

    email_template = 'privacy/records_access_email.html'
    def format_subject(self, name):
        return f'Records request from consumerfinance.gov: {name}'

    def email_body(self, data):
        num_files = len(data['uploaded_files'])
        data.update({'num_files': num_files,
            'consent_text':self.consent_text})
        return loader.render_to_string(self.email_template, data)
