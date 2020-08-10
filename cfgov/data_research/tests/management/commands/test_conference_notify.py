from io import StringIO

from django.core import mail
from django.core.management import call_command
from django.test import TestCase


class ConferenceNotifyTests(TestCase):
    fixtures = [
        'conference_registrants.json',
        'conference_registration_page.json',
    ]

    def test_sends_email(self):
        call_command(
            'conference_notify',
            '99999',
            '--to-email=to@unit.test',
            verbosity=0
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            '[2018 CFPB FinEx Conference] Attendance Update'
        )
        self.assertEqual(mail.outbox[0].from_email, 'donotreply@cfpb.gov')
        self.assertEqual(mail.outbox[0].to, ['to@unit.test'])

    def test_writes_to_stdout(self):
        out = StringIO()
        call_command(
            'conference_notify',
            '99999',
            '--to-email=to@unit.test',
            stdout=out
        )
        self.assertIn('Attendance Update', out.getvalue())
