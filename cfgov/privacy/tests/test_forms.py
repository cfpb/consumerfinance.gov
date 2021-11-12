from django.utils.datastructures import MultiValueDict
from django.test import TestCase

from privacy.forms import DisclosureConsentForm, RecordsAccessForm


class RecordsAccessFormTests(TestCase):
    minimum_data = {
        'description': 'This is a description of the desired records',
        'requestor_name': 'Example Person',
        'requestor_email': "person@example.com",
        'contact_channel': 'email',
        'full_name': 'Example Q. Person',
        'consent': True,
    }

    minimum_files = MultiValueDict({
        "supporting_documentation": []
    })

    def test_valid_data_has_no_errors(self):
        form = RecordsAccessForm(
            data=self.minimum_data,
            files=self.minimum_files
        )
        self.assertTrue(form.is_valid())

    def test_mailing_address_required(self):
        data = self.minimum_data
        data.update({'contact_channel': 'mail'})
        form = RecordsAccessForm(
            data=data,
            files=self.minimum_files
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Mailing address is required if requesting records by mail.',
            form.errors['street_address'])

    def test_satisfied_mailing_address_requirement(self):
        data = self.minimum_data
        data.update({
            'contact_channel': 'mail',
            'street_address': '101 Example Ave.',
            'city': 'Washington',
            'state': 'DC',
            'zip_code': '20002',
        })

        form = RecordsAccessForm(
            data=data,
            files=self.minimum_files
        )
        self.assertTrue(form.is_valid())

    def test_email_subject(self):
        data = self.minimum_data
        form = RecordsAccessForm(
            data=data,
            files=self.minimum_files
        )
        self.assertEqual(
            form.format_subject(self.minimum_data['requestor_name']),
            'Records request from consumerfinance.gov: Example Person'
        )

    def test_email_body(self):
        data = self.minimum_data
        data.update({'uploaded_files': []})
        form = RecordsAccessForm(
            data=data,
            files=self.minimum_files
        )
        self.assertIn(
            'h1>Request for individual access to records protected under the Privacy Act</h1>', #noqa: E501
            form.email_body(self.minimum_data),
        )
        self.assertIn(
            'person@example.com',
            form.email_body(self.minimum_data),
        )


class DisclosureConsentFormTests(TestCase):
    minimum_data = {
        'description': 'This is a description of the desired records',
        'requestor_name': 'Example Person',
        'requestor_email': "person@example.com",
        'recipient_name': 'Person Q. Name',
        'recipient_email': 'email@example.com',
        'contact_channel': 'email',
        'full_name': 'Example Q. Person',
        'consent': True,
    }

    minimum_files = MultiValueDict({
        "supporting_documentation": []
    })

    def test_valid_data_has_no_errors(self):
        form = DisclosureConsentForm(
            data=self.minimum_data,
            files=self.minimum_files
        )
        self.assertTrue(form.is_valid())

    def test_disclosure_consent_form_requires_additional_fields(self):
        invalid_data = {
            'description': 'This is a description of the desired records',
            'requestor_name': 'Example Person',
            'requestor_email': "person@example.com",
            'recipient_name': 'Person Q. Name',
            'recipient_email': '',
            'contact_channel': 'email',
            'full_name': 'Example Q. Person',
            'consent': True,
        }
        form = DisclosureConsentForm(
            data=invalid_data,
            files=self.minimum_files
        )
        self.assertFalse(form.is_valid())

    def test_email_subject(self):
        form = DisclosureConsentForm(
            data=self.minimum_data,
            files=self.minimum_files
        )
        self.assertEqual(
            form.format_subject(self.minimum_data['requestor_name']),
            'Disclosure request from consumerfinance.gov: Example Person'
        )

    def test_email_body(self):
        data = self.minimum_data
        self.minimum_data.update({'uploaded_files': []})
        form = DisclosureConsentForm(
            data=data,
            files=self.minimum_files
        )
        self.assertIn(
            'person@example.com',
            form.email_body(self.minimum_data),
        )
        self.assertIn(
            '<h1>Consent for disclosure of records protected under the Privacy Act</h1>',  #noqa: E501
            form.email_body(self.minimum_data),
        )
