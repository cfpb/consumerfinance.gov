from django.test import TestCase

from core.govdelivery import MockGovDelivery
from data_research.forms import ConferenceRegistrationForm
from data_research.models import ConferenceRegistration


class ConferenceRegistrationFormTests(TestCase):
    capacity = 100
    govdelivery_code = 'TEST-CODE'
    govdelivery_question_id = '12345'
    govdelivery_answer_id = '67890'

    def test_invalid_form_if_fields_are_missing(self):
        form = ConferenceRegistrationForm(
            capacity=self.capacity,
            govdelivery_code=self.govdelivery_code,
            govdelivery_question_id=self.govdelivery_question_id,
            govdelivery_answer_id=self.govdelivery_answer_id,
            data={'foo': 'bar'}
        )
        self.assertFalse(form.is_valid())

    def get_valid_form(
        self,
        attendee_type=ConferenceRegistrationForm.ATTENDEE_IN_PERSON,
        govdelivery_question_id=None,
        govdelivery_answer_id=None
    ):
        return ConferenceRegistrationForm(
            capacity=self.capacity,
            govdelivery_code=self.govdelivery_code,
            govdelivery_question_id=govdelivery_question_id,
            govdelivery_answer_id=govdelivery_answer_id,
            data={
                'attendee_type': attendee_type,
                'name': 'A User',
                'organization': 'An Organization',
                'email': 'user@domain.com',
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
            'attendee_type': ConferenceRegistrationForm.ATTENDEE_IN_PERSON,
            'name': 'A User',
            'organization': 'An Organization',
            'email': 'user@domain.com',
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

    def test_form_save_commit_true_subscribes_and_sets_question(self):
        form = self.get_valid_form(
            govdelivery_question_id='12345',
            govdelivery_answer_id='67890'
        )
        form.is_valid()
        form.save()

        self.assertEqual(MockGovDelivery.calls, [
            (
                'set_subscriber_topics',
                (),
                {
                    'contact_details': 'user@domain.com',
                    'topic_codes': ['TEST-CODE'],
                    'send_notifications': True,
                }
            ),
            (
                'set_subscriber_answer_to_select_question',
                (),
                {
                    'contact_details': 'user@domain.com',
                    'question_id': '12345',
                    'answer_id': '67890',
                }
            ),
        ])

    def make_capacity_registrants(self, govdelivery_code, attendee_type):
        registrant = ConferenceRegistration(
            govdelivery_code=govdelivery_code,
            details={'attendee_type': attendee_type}
        )
        ConferenceRegistration.objects.bulk_create(
            [registrant] * self.capacity
        )

    def test_form_not_at_capacity(self):
        self.assertFalse(self.get_valid_form().at_capacity)

    def test_form_at_capacity(self):
        self.make_capacity_registrants(
            self.govdelivery_code,
            ConferenceRegistrationForm.ATTENDEE_IN_PERSON
        )
        self.assertTrue(self.get_valid_form().at_capacity)

    def test_form_at_capacity_for_some_other_code(self):
        self.make_capacity_registrants(
            'some-other-code',
            ConferenceRegistrationForm.ATTENDEE_IN_PERSON
        )
        self.assertFalse(self.get_valid_form().at_capacity)

    def test_form_at_capacity_invalid(self):
        self.make_capacity_registrants(
            self.govdelivery_code,
            ConferenceRegistrationForm.ATTENDEE_IN_PERSON
        )
        form = self.get_valid_form()
        self.assertFalse(form.is_valid())

    def test_form_at_capacity_still_valid_for_virtual_attendees(self):
        self.make_capacity_registrants(
            self.govdelivery_code,
            ConferenceRegistrationForm.ATTENDEE_IN_PERSON
        )
        form = self.get_valid_form(
            attendee_type=ConferenceRegistrationForm.ATTENDEE_VIRTUALLY
        )
        self.assertTrue(form.is_valid())

    def test_form_virtual_attendees_dont_count_against_capacity(self):
        self.make_capacity_registrants(
            self.govdelivery_code,
            ConferenceRegistrationForm.ATTENDEE_VIRTUALLY
        )
        self.assertFalse(self.get_valid_form().at_capacity)
