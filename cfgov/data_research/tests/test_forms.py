from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from core.govdelivery import MockGovDelivery
from data_research.forms import ConferenceRegistrationForm
from data_research.models import ConferenceRegistration


class ConferenceRegistrationFormTests(TestCase):
    govdelivery_code = 'TEST-CODE'

    def test_invalid_form_if_fields_are_missing(self):
        form = ConferenceRegistrationForm(
            govdelivery_code=self.govdelivery_code,
            data={'foo': 'bar'}
        )
        self.assertFalse(form.is_valid())

    def get_valid_form(self):
        return ConferenceRegistrationForm(
            govdelivery_code=self.govdelivery_code,
            data={
                'name': 'A User',
                'organization': 'An Organization',
                'email': 'user@domain.com',
                'sessions': ['Thursday morning', 'Thursday lunch'],
            }
        )

    def test_valid_form_if_required_fields_are_provided(self):
        form = self.get_valid_form()
        self.assertTrue(form.is_valid())

    def test_form_save_commit_false_doesnt_save_user(self):
        form = self.get_valid_form()
        form.is_valid()
        form.save(commit=False)
        self.assertFalse(ConferenceRegistration.objects.exists())

    def test_form_save_commit_false_doesnt_subscribe_to_govdelivery(self):
        calls_before = list(MockGovDelivery.calls)
        form = self.get_valid_form()
        form.is_valid()
        form.save(commit=False)
        self.assertEqual(MockGovDelivery.calls, calls_before)

    def test_form_save_sets_registration_code_and_details(self):
        form = self.get_valid_form()
        form.is_valid()
        registrant = form.save(commit=False)

        self.assertEqual(registrant.govdelivery_code, 'TEST-CODE')
        self.assertEqual(registrant.details, {
            'name': 'A User',
            'organization': 'An Organization',
            'email': 'user@domain.com',
            'sessions': ['Thursday morning', 'Thursday lunch'],
            'dietary_restrictions': [],
            'other_dietary_restrictions': '',
            'accommodations': [],
            'other_accommodations': '',
        })

    def test_form_save_commit_true_saves_to_db(self):
        form = self.get_valid_form()
        form.is_valid()
        registrant = form.save()

        self.assertEqual(registrant, ConferenceRegistration.objects.first())

    def test_form_save_commit_true_subscribes_to_gd(self):
        form = self.get_valid_form()
        form.is_valid()
        form.save()

        self.assertEqual(
            MockGovDelivery.calls,
            [(
                'set_subscriber_topics',
                (),
                {
                    'contact_details': 'user@domain.com',
                    'topic_codes': ['TEST-CODE'],
                    'send_notifications': True,
                }
            )]
        )
