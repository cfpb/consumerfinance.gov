from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(
    FLAGS={'PRIVACY_FORMS': [('boolean', True)]},
    PRIVACY_EMAIL_TARGET='email@foia.gov',
)
class TestRecordsAccessForm(TestCase):
    def test_get_the_form(self):
        response = self.client.get(reverse('privacy:records_access'))
        self.assertContains(
            response,
            'Request for individual access to records protected under the Privacy Act'  # noqa: E501
        )

    def test_invalid_form_post_does_not_send_email(self):
        self.client.post(
            reverse('privacy:records_access'),
            {
                'description': '',
                'system_of_record': '',
                'requestor_name': '',
                'requestor_email': '',
                'contact_channel': 'mail',
            },
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_valid_form_post_sends_email_and_redirects(self):
        response = self.client.post(
            reverse('privacy:records_access'),
            {
                'description': 'This is a description of the desired records',
                'requestor_name': 'Example Person',
                'requestor_email': 'person@example.com',
                'contact_channel': 'email',
                'full_name': 'Example Q. Person',
                'consent': True,
                'supporting_documentation': []
            },
        )

        email = mail.outbox[0]
        self.assertEqual(
            email.subject,
            'Records request from consumerfinance.gov: Example Person',
        )
        self.assertIn('Example Q. Person', email.body)
        self.assertEqual(email.to, ['email@foia.gov'])
        self.assertEqual(email.reply_to, ['person@example.com'])
        self.assertRedirects(response, reverse('privacy:form_submitted'))


@override_settings(
    FLAGS={'PRIVACY_FORMS': [('boolean', True)]},
    PRIVACY_EMAIL_TARGET='email@foia.gov',
)
class TestDisclosureConsentForm(TestCase):
    def test_get_the_form(self):
        response = self.client.get(reverse('privacy:disclosure_consent'))
        self.assertContains(
            response,
            'Consent for disclosure of records protected under the Privacy Act'
        )

    def test_invalid_form_post_does_not_send_email(self):
        self.client.post(
            reverse('privacy:disclosure_consent'),
            {
                'description': '',
                'system_of_record': '',
                'requestor_name': '',
                'requestor_email': '',
                'recipient_name': 'Recipient Person',
                'recipient_email': 'recipient@example.com',
                'contact_channel': 'mail',
            },
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_valid_form_post_sends_email_and_redirects(self):
        response = self.client.post(
            reverse('privacy:disclosure_consent'),
            {
                'description': 'This is a description of the desired records',
                'requestor_name': 'Example Person',
                'requestor_email': 'person@example.com',
                'recipient_name': 'Recipient Person',
                'recipient_email': 'recipient@example.com',
                'contact_channel': 'email',
                'full_name': 'Example Q. Person',
                'consent': True,
                'supporting_documentation': []
            },
        )

        email = mail.outbox[0]
        self.assertEqual(
            email.subject,
            'Disclosure request from consumerfinance.gov: Example Person',
        )
        self.assertIn('Recipient Person', email.body)
        self.assertEqual(email.to, ['email@foia.gov'])
        self.assertEqual(email.reply_to, ['person@example.com'])
        self.assertRedirects(response, reverse('privacy:form_submitted'))
