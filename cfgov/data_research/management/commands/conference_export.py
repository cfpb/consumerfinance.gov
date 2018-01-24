from __future__ import print_function

import csv
import json
import logging
from cStringIO import StringIO

from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.utils.encoding import force_bytes

from wagtail.wagtailcore.models import Page

from data_research.models import ConferenceRegistration
from v1.util.migrations import get_stream_data


logger = logging.getLogger(__name__)


def get_registration_form_from_page(page_id):
    page = Page.objects.get(pk=page_id).specific
    content = get_stream_data(page, 'content')

    for block in content:
        if 'conference_registration_form' == block['type']:
            return block

    raise RuntimeError('no registration form found on {}'.format(page))


class ConferenceExporter(object):
    FIELDS = (
        ('name', 'Name'),
        ('organization', 'Organization'),
        ('email', 'Email Address'),
        ('sessions', 'Selected Sessions'),
        ('foodinfo', 'Food Restrictions'),
        ('accommodations', 'Accommodations Needed'),
        ('code', 'GovDelivery Code'),
    )

    EMAIL_SUBJECTS = (
        '[2016 CFPB Research Conference] Attendance Update',
        '[2016 CFPB Research Conference] Attendance Full',
    )

    EMAIL_BODIES = (
        (
            'The 2016 Research Conference is at {0.count} of '
            '{0.conference_capacity} capacity for signups.'
        ),
        (
            'The 2016 Research Conference has reached capacity with {0.count} '
            'submissions. Signups are now closed.\n\nThe capacity for this '
            'event was set to {0.conference_capacity} at the time of this '
            'email.'
        ),
    )

    EMAIL_FOOTER = (
        '\n\nSee attached for attendee details.\n\n'
        'This is an automated message.'
    )

    ATTACHMENT_FILENAME = 'conference_registrations.csv'

    def __init__(self, page_id, verbose=False):
        self.form_block = get_registration_form_from_page(page_id)
        self.verbose = verbose

        if self.verbose:
            logger.info('conference code {}'.format(self.conference_code))
            logger.info('capacity {}'.format(self.conference_capacity))

    @property
    def conference_code(self):
        return self.form_block['value']['code']

    @property
    def conference_capacity(self):
        return self.form_block['value']['capacity']

    @property
    def at_capacity(self):
        return self.count >= self.conference_capacity

    @property
    def attendees(self):
        return ConferenceRegistration.objects.filter(code=self.conference_code)

    @property
    def count(self):
        return self.attendees.count()

    def to_csv(self):
        if self.verbose:
            logger.info('generating CSV for {} attendees'.format(self.count))

        csvfile = StringIO()
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow([field[1] for field in self.FIELDS])

        for attendee in self.attendees:
            writer.writerow(self.attendee_to_row(attendee))

        return csvfile.getvalue()

    @classmethod
    def attendee_to_row(cls, attendee):
        return [cls.prepare_field(attendee, field[0]) for field in cls.FIELDS]

    @staticmethod
    def prepare_field(attendee, field):
        value = getattr(attendee, field)

        if 'sessions' == field:
            value = ','.join(json.loads(value or '[]'))

        return force_bytes(value)

    def create_email_message(self, from_address, to_addresses):
        subject = self.EMAIL_SUBJECTS[self.at_capacity]
        body = self.EMAIL_BODIES[self.at_capacity] + self.EMAIL_FOOTER
        body = body.format(self)

        csvfile = self.to_csv()

        message = EmailMessage(subject, body, from_address, to_addresses)
        message.attach(self.ATTACHMENT_FILENAME, csvfile, 'text/csv')

        return message


class Command(BaseCommand):
    help = 'Exports conference registration attendees via CSV or email'

    def add_arguments(self, parser):  # pragma: no cover
        parser.add_argument(
            'page_id',
            help='Wagtail page primary key containing registration form'
        )
        parser.add_argument(
            '-f', '--email-from-address',
            default='donotreply@cfpb.gov',
            help='From email address (default %(default)s)'
        )
        parser.add_argument(
            '-t', '--email-to-address',
            nargs='*',
            help='To email address (optional, may specify multiple)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Create and display email but do not send'
        )

    def handle(self, *args, **options):
        page_id = options['page_id']
        verbose = options['verbosity'] >= 2
        email_from_address = options['email_from_address']
        email_to_addresses = options['email_to_address']
        dry_run = options['dry_run']

        exporter = ConferenceExporter(page_id=page_id, verbose=verbose)

        if email_to_addresses:
            if verbose:
                print('Sending email from', email_from_address)
                print('Sending email to', email_to_addresses)

            message = exporter.create_email_message(
                from_address=email_from_address,
                to_addresses=email_to_addresses
            )

            if dry_run:
                print('From:', message.from_email)
                print('To:', ', '.join(message.to))
                print('Subject:', message.subject)
                print(message.body)
            else:
                message.send()
        else:
            print(exporter.to_csv(), end='')
