import re

from django.core.mail import EmailMessage
from django.template import loader
from django.utils.functional import cached_property

import wagtail
from wagtail.core.models import Page

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from data_research.forms import ConferenceRegistrationForm
from data_research.models import ConferenceRegistration


def get_conference_details_from_page(page_id):
    """Retrieve conference details from a Wagtail registration page.

    This function takes a Wagtail page ID, finds the
    ConferenceRegistrationForm block type contained that page's primary
    StreamField (`page.content`), and returns its configuration as a dict.
    """
    page = Page.objects.get(pk=page_id).specific

    if hasattr(page, 'content'):
        if wagtail.VERSION < (2, 12):
            data = page.content.stream_data
        else:
            data = page.content.raw_data
        for block in data:
            if 'conference_registration_form' == block['type']:
                return {
                    key: block['value'][key]
                    for key in ('govdelivery_code', 'capacity')
                }

    raise RuntimeError('no registration form found on %s' % page)


class ConferenceExporter(object):
    """Generates a Excel workbook of registrants for a given conference.

    Looks up conference attendees by GovDelivery code.
    """
    def __init__(self, govdelivery_code):
        self.govdelivery_code = govdelivery_code

    @cached_property
    def registrants(self):
        return ConferenceRegistration.objects.filter(
            govdelivery_code=self.govdelivery_code
        )

    @cached_property
    def fields(self):
        form = ConferenceRegistrationForm(
            govdelivery_code=self.govdelivery_code,
            govdelivery_question_id=None,
            govdelivery_answer_id=None,
            capacity=0
        )

        return ['created'] + list(form.fields.keys())

    def save_xlsx(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.get_xlsx_bytes())

    def get_xlsx_bytes(self):
        workbook = Workbook()
        workbook.guess_types = True
        worksheet = workbook.active

        worksheet.append(self.fields)

        for registrant in self.registrants:
            worksheet.append(self._registrant_to_row(registrant))

        return bytes(save_virtual_workbook(workbook))

    def _registrant_to_row(self, registrant):
        return [registrant.created] + [
            self._prep_value(registrant.details.get(key))
            for key in self.fields[1:]
        ]

    def _prep_value(self, value):
        return ', '.join(value) if isinstance(value, list) else value


class ConferenceNotifier(object):
    """Emails an Excel workbook of registrants for a given conference.

    Looks up conference attendees by GovDelivery code.
    """
    conference_name = '2018 CFPB FinEx Conference'
    subject_template_name = 'data_research/conference_notify_subject.txt'
    email_template_name = 'data_research/conference_notify_email.txt'
    attachment_filename = 'conference_registrations.xlsx'
    attachment_mimetype = (
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    def __init__(self, govdelivery_code, capacity):
        exporter = ConferenceExporter(govdelivery_code)

        self.count = exporter.registrants.count()
        self.count_in_person = len(list(exporter.registrants.in_person()))
        self.count_virtual = len(list(exporter.registrants.virtual()))
        self.capacity = capacity

        if self.count:
            self.attachment_bytes = exporter.get_xlsx_bytes()

    def create_email(self, from_email, to_emails):
        context = {
            'conference_name': self.conference_name,
            'count': self.count,
            'count_in_person': self.count_in_person,
            'count_virtual': self.count_virtual,
            'capacity': self.capacity,
            'at_capacity': self.count_in_person >= self.capacity,
        }

        subject = loader.render_to_string(self.subject_template_name, context)
        # Email subject must not contain newlines.
        subject = ''.join(subject.splitlines()).strip()

        body = loader.render_to_string(self.email_template_name, context)
        # Condense multiple blank lines in body.
        body = re.sub(r'\n\n+', '\n\n', body).strip()

        email_message = EmailMessage(subject, body, from_email, to_emails)

        if self.count:
            email_message.attach(
                self.attachment_filename,
                self.attachment_bytes,
                self.attachment_mimetype
            )

        return email_message
