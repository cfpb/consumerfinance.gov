import json

from django.http import HttpResponseRedirect
from django.test import RequestFactory, TestCase

from mock import Mock, patch

from data_research.forms import ConferenceRegistrationForm
from data_research.handlers import ConferenceRegistrationHandler
from data_research.models import ConferenceRegistration


class TestConferenceRegistrationHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.page = Mock()
        self.path = '/path/to/page'

        govdelivery_patcher = patch('data_research.handlers.GovDelivery')
        self.patched_govdelivery = govdelivery_patcher.start()
        self.addCleanup(govdelivery_patcher.stop)

        self.post_data = {
            'name': 'Generic User',
            'organization': 'Data Research Inst',
            'email': 'user@example.com',
            'form_sessions': ['0', '1', '2'],
            'foodinfo': 'N/A',
            'accommodations': 'N/A',
            'code': 'ABC123',
        }

        self.capacity = 100
        self.block_value = {
            'capacity': self.capacity,
            'code': 'ABC123',
            'sessions': [
                'Session 0 description',
                'Session 1 description',
                'Session 2 description'
            ],
            'failure_message': 'Something went wrong.',
        }

    def get_handler(self, request=None, post_data=None):
        if post_data is None:
            post_data = self.post_data

        if request is None:
            request = self.factory.post(self.path, post_data)

        return ConferenceRegistrationHandler(
            page=self.page,
            request=request,
            block_value=self.block_value
        )

    def make_registrants(self, handler, count, code=None):
        code = code or handler.block_value['code']
        ConferenceRegistration.objects.bulk_create(
            [ConferenceRegistration(code=code)] * count
        )

    def test_capacity_not_reached_no_registrations_yet(self):
        handler = self.get_handler()
        self.assertFalse(handler.is_at_capacity())

    def test_capacity_not_reached(self):
        handler = self.get_handler()
        self.make_registrants(handler, self.capacity - 1)
        self.assertFalse(handler.is_at_capacity())

    def test_capacity_reached(self):
        handler = self.get_handler()
        self.make_registrants(handler, self.capacity)
        self.assertTrue(handler.is_at_capacity())

    def test_capacity_not_reached_for_other_codes(self):
        handler = self.get_handler()
        self.make_registrants(handler, self.capacity, code='a-different-code')
        self.assertFalse(handler.is_at_capacity())

    def test_is_successful_submission_default_false(self):
        request = self.factory.get('/')
        handler = self.get_handler(request)
        self.assertFalse(handler.is_successful_submission())

    def test_is_successful_submission_query_string_true(self):
        request = self.factory.get('/?success')
        handler = self.get_handler(request)
        self.assertTrue(handler.is_successful_submission())

    def test_at_capacity_returns_flag_by_default(self):
        handler = self.get_handler()
        self.make_registrants(handler, self.capacity)
        result = handler.process(False)
        self.assertTrue(result.get('is_at_capacity'))

    def test_at_capacity_returns_flag_on_submission(self):
        handler = self.get_handler()
        self.make_registrants(handler, self.capacity)
        result = handler.process(True)
        self.assertTrue(result.get('is_at_capacity'))

    def test_not_at_capacity_does_not_return_flag(self):
        handler = self.get_handler()
        result = handler.process(False)
        self.assertFalse(result.get('is_at_capacity'))

    def test_process_returns_redirect(self):
        handler = self.get_handler()
        result = handler.process(True)
        self.assertIsInstance(result, HttpResponseRedirect)

    def test_process_returns_temporary_redirect(self):
        handler = self.get_handler()
        result = handler.process(True)
        self.assertEqual(result.status_code, 302)

    def test_process_returns_redirect_with_query_string_parameter(self):
        handler = self.get_handler()
        result = handler.process(True)
        self.assertEqual(result['Location'], self.path + '?success')

    def test_process_creates_registrant(self):
        self.assertFalse(ConferenceRegistration.objects.exists())
        handler = self.get_handler()
        handler.process(True)
        self.assertEqual(ConferenceRegistration.objects.count(), 1)

    def test_process_sets_registrant_from_post_data(self):
        handler = self.get_handler()
        handler.process(True)
        attendee = ConferenceRegistration.objects.first()
        self.assertEqual(attendee.name, self.post_data['name'])
        self.assertEqual(
            attendee.organization,
            self.post_data['organization']
        )
        self.assertEqual(attendee.email, self.post_data['email'])
        self.assertEqual(
            attendee.sessions,
            json.dumps(self.block_value['sessions'])
        )
        self.assertEqual(attendee.foodinfo, self.post_data['foodinfo'])
        self.assertEqual(
            attendee.accommodations,
            self.post_data['accommodations']
        )
        self.assertEqual(attendee.code, self.post_data['code'])

    def test_unsubmitted_process_returns_empty_form(self):
        handler = self.get_handler()
        result = handler.process(False)
        self.assertIsInstance(result['form'], ConferenceRegistrationForm)
        self.assertFalse(result['form'].is_bound)

    def test_get_post_data_returns_dict(self):
        handler = self.get_handler()
        result = handler.get_post_data()
        self.assertIsInstance(result, dict)

    def test_get_post_data_sets_sessions_from_form_sessions(self):
        handler = self.get_handler()

        with patch(
            'data_research.handlers.ConferenceRegistrationHandler.'
            'get_sessions',
            return_value=handler.block_value['sessions']
        ):
            result = handler.get_post_data()
            self.assertEqual(
                result['sessions'],
                json.dumps(handler.block_value['sessions'])
            )

    def test_failed_govdelivery_sets_form_error(self):
        with patch(
            'data_research.handlers.ConferenceRegistrationHandler.subscribe',
            return_value=False
        ):
            handler = self.get_handler()
            result = handler.process(True)
            self.assertTrue(result['form'].non_field_errors)

    def test_subscribe_instantiates_GovDelivery_with_account_code(self):
        with self.settings(ACCOUNT_CODE='abcde'):
            handler = self.get_handler()
            handler.subscribe('em@il.com', 'code')
            self.patched_govdelivery.assert_called_with(account_code='abcde')

    def test_subscribe_sets_subscriptions(self):
        handler = self.get_handler()
        handler.subscribe('em@il.com', 'code')
        mock_govdelivery = self.patched_govdelivery.return_value
        mock_govdelivery.set_subscriber_topics.assert_called_with(
            email_address='em@il.com',
            topic_codes=['code'],
            send_notifications=True,
        )

    def test_subscribe_returns_true_for_success(self):
        mock_govdelivery = self.patched_govdelivery.return_value
        mock_govdelivery.set_subscriber_topics.return_value.status_code = 200
        handler = self.get_handler()
        self.assertTrue(handler.subscribe('em@il.com', 'code'))

    def test_subscribe_returns_false_for_failure(self):
        mock_govdelivery = self.patched_govdelivery.return_value
        mock_response = mock_govdelivery.set_subscriber_topics()
        mock_response.raise_for_status.side_effect = RuntimeError
        handler = self.get_handler()
        self.assertFalse(handler.subscribe('em@il.com', 'code'))

    def test_get_sessions_returns_strings_from_block_value(self):
        request = self.factory.post(self.path, {'form_sessions': ['0']})
        handler = self.get_handler(request)
        sessions = handler.get_sessions()
        self.assertEqual(sessions, ['Session 0 description'])
