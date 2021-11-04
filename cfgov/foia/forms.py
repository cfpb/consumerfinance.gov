from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse


# Form input attributes for Design System compatibility.
# Technique copied from data_research/forms.py
#
# See https://cfpb.github.io/design-system/components/text-inputs
# for documentation on the styles that are being duplicated here.
text_input_attrs = {
    'class': 'a-text-input a-text-input__full',
}

class FoiaRequestForm(forms.Form):
    requester_name = forms.CharField(
        label='Requester name',
        help_text='The individual consenting to the privacy act statement',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    subject_line = forms.CharField(
        label='Subject line',
        widget=forms.TextInput(attrs=text_input_attrs),
    )
    request_description = forms.CharField(
        label='Description of FOIA request',
        widget=forms.Textarea(attrs=text_input_attrs),
    )
    file_upload = forms.FileField(
        label='Upload supplementary information',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )
    privacy_consent = forms.BooleanField(
        label='I consent to the privacy statement',
        required=False,
        widget=forms.CheckboxInput(),
    )

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
            display_size = round(total_uploaded_bytes/mb, 1)
            err = forms.ValidationError(
                    f"Total size of uploaded files ({display_size} MB) was greater than size limit (2 MB).")
            self.add_error('file_upload', err)

    def limit_number_of_files(self, files):
        max_files = 6
        if len(files) > max_files:
            err = forms.ValidationError(
                    f"Please choose {max_files} or fewer files. You chose {len(files)}.")
            self.add_error('file_upload', err)


    def clean(self):
        cleaned_data = super().clean()
        uploaded_files = self.files.getlist('file_upload')
        self.limit_file_size(uploaded_files)
        self.limit_number_of_files(uploaded_files)

    def send_email(self):
        subject = 'Online FOIA request: ' + self.cleaned_data['subject_line']
        body = 'The following information was submitted via web form on ' + \
                  'consumerfinance.gov/foia/foia-request-form. Any ' + \
                  'attachments have not been scanned for viruses and may be ' + \
                  'unsafe. \n\n'
        from_email = settings.DEFAULT_FROM_EMAIL
        # recipient_list = ['FOIA@consumerfinance.gov']
        recipient_list = ['elizabeth.lorton@cfpb.gov']

        for (name, field) in self.fields.items():
            body += field.label + ': ' + str(self.cleaned_data[name]) + '\n'

        email = EmailMessage(subject, body, from_email, recipient_list)
        uploaded_files = self.files.getlist('file_upload')
        for f in uploaded_files:
            email.attach(f.name, f.read(), f.content_type)

        try:
            email.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
