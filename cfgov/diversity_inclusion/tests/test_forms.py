from django.test import TestCase

from diversity_inclusion.forms import VoluntaryAssessmentForm


class TestVoluntaryAssessmentForm(TestCase):
    def test_empty_data_is_invalid(self):
        post_data = {}

        form = VoluntaryAssessmentForm(post_data)
        self.assertFalse(form.is_valid())

    def test_partial_data_is_invalid(self):
        post_data = {
            # not all required fields are filled out
            'institution_name': 'Institution Name',
        }

        form = VoluntaryAssessmentForm(post_data)
        self.assertFalse(form.is_valid())

    def test_invalid_email_address_is_invalid(self):
        post_data = {
            # data is in the wrong format to get a score back
            'institution_name': 'Institution Name',
            'institution_address': '123 Main Street',
            'institution_city': 'Anytown',
            'institution_state': 'NA',
            'institution_zip': '12345',
            'tax_id': '123456789',
            'contact_name': 'Human Being',
            'contact_title': 'Job Title',
            'contact_email': 'Email Address',
            'contact_phone': '(123) 456-7890',
            'contact_phone_alt': '',
        }

        form = VoluntaryAssessmentForm(post_data)
        self.assertFalse(form.is_valid())

    def test_correct_data_is_valid(self):
        post_data = {
            'institution_name': 'Institution Name',
            'institution_address': '123 Main Street',
            'institution_city': 'Anytown',
            'institution_state': 'NA',
            'institution_zip': '12345',
            'tax_id': '123456789',
            'contact_name': 'Human Being',
            'contact_title': 'Job Title',
            'contact_email': 'human.being@instituion.name',
            'contact_phone': '(123) 456-7890',
            'contact_phone_alt': '',
        }

        form = VoluntaryAssessmentForm(post_data)
        self.assertTrue(form.is_valid())
