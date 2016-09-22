import mock
from django.test import RequestFactory, TestCase

from ..handlers import ConferenceRegistrationHandler as Handler


class TestConferenceRegistrationHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        page = mock.Mock()
        post_data = {
            'name': 'Kurt Wall',
            'organization': 'Excella Consulting',
            'email': 'kurt@mail.com',
            'form_sessions': ['0', '1', '2'],
            'foodinfo': 'N/A',
            'accommodations': 'N/A',
            'codes': ['ABC123', 'QWE321']
        }
        request = self.factory.post('/', post_data)
        block_value = {
            'sessions': [
                'Session 0 description',
                'Session 1 description',
                'Session 2 description'
            ]
        }
        self.handler = Handler(page, request, block_value)

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_post_data')
    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_response')
    @mock.patch('data_research.handlers.ConferenceRegistrationForm')
    def test_process_calls_get_post_data_for_submitted_form(self, mock_form, mock_get_response, mock_get_post_data):
        self.handler.process(is_submitted=True)
        assert mock_get_post_data.called

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_post_data')
    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_response')
    @mock.patch('data_research.handlers.ConferenceRegistrationForm')
    def test_process_binds_form_for_submissions(self, mock_form, mock_get_response, mock_get_post_data):
        data = {'post_data': None}
        mock_get_post_data.return_value = data
        self.handler.process(is_submitted=True)
        mock_form.assert_called_with(data)

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_post_data')
    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_response')
    @mock.patch('data_research.handlers.ConferenceRegistrationForm')
    def test_process_calls_get_response_for_submissions(self, mock_form, mock_get_response, mock_get_post_data):
        self.handler.process(is_submitted=True)
        mock_get_response.assert_called_with(mock_form())

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_post_data')
    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_response')
    @mock.patch('data_research.handlers.ConferenceRegistrationForm')
    def test_process_does_not_bind_form_non_submissions(self, mock_form, mock_get_response, mock_get_post_data):
        self.handler.process(is_submitted=False)
        mock_form.assert_called_with()

    @mock.patch('data_research.handlers.ConferenceRegistrationForm')
    def test_process_returns_context(self, mock_form):
        result = self.handler.process(False)
        self.assertEqual(result, {'form': mock_form()})

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_response')
    def test_process_returns_get_response_call_for_submission(self, mock_get_response):
        result = self.handler.process(True)
        self.assertEqual(result, mock_get_response())

    def test_get_post_data_returns_dict(self):
        result = self.handler.get_post_data()
        self.assertIsInstance(result, dict)

    def test_get_post_data_sets_sessions_from_form_sessions(self):
        result = self.handler.get_post_data()
        assert 'sessions' in result
        session_str = ','.join(result.getlist('form_sessions'))
        self.assertEqual(session_str, result['sessions'])

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.fail')
    def test_get_response_calls_form_isvalid(self, mock_fail):
        form = mock.Mock()
        form.is_valid.return_value = False
        self.handler.get_response(form)
        self.assertTrue(form.is_valid.called)

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.fail')
    def test_get_response_calls_calls_fail_for_invalid_form(self, mock_fail):
        form = mock.Mock()
        form.is_valid.return_value = False
        self.handler.get_response(form)
        mock_fail.assert_called_with(form)

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.subscribe')
    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.fail')
    def test_get_response_calls_subscribe(self, mock_fail, mock_subscribe):
        form = mock.Mock()
        mock_subscribe.return_value = False
        self.handler.get_response(form)
        mock_subscribe.assert_called_with(form.save().email, ['ABC123', 'QWE321'])

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.subscribe')
    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.fail')
    def test_get_response_calls_fail_for_failed_subscribe(self, mock_fail, mock_subscribe):
        form = mock.Mock()
        mock_subscribe.return_value = False
        self.handler.get_response(form)
        mock_fail.assert_called_with(form)

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.success')
    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.save_attendee')
    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.subscribe')
    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.fail')
    def test_get_response_calls_save_attendee_and_success_for_successful_subscription(self, mock_fail, mock_subscribe, mock_save_attendee, mock_success):
        form = mock.Mock()
        mock_subscribe.return_value = True
        self.handler.get_response(form)
        mock_save_attendee.assert_called_with(form.save())
        self.assertTrue(mock_success.called)

    @mock.patch('data_research.handlers.settings')
    @mock.patch('data_research.handlers.messages')
    @mock.patch('data_research.handlers.GovDelivery')
    def test_subscribe_instantiates_GovDelivery_with_account_code(self, mock_gd, mock_messages, mock_settings):
        self.handler.subscribe('em@il.com', ['code'])
        mock_gd.assert_called_with(account_code=mock_settings.ACCOUNT_CODE)

    @mock.patch('data_research.handlers.settings')
    @mock.patch('data_research.handlers.messages')
    @mock.patch('data_research.handlers.GovDelivery')
    def test_subscribe_sets_subscriptions(self, mock_gd, mock_messages, mock_settings):
        self.handler.subscribe('em@il.com', ['code'])
        mock_gd().set_subscriber_topics.assert_called_with('em@il.com', ['code'])

    @mock.patch('data_research.handlers.settings')
    @mock.patch('data_research.handlers.messages')
    @mock.patch('data_research.handlers.GovDelivery')
    def test_subscribe_returns_True_for_success(self, mock_gd, mock_messages, mock_settings):
        mock_gd().set_subscriber_topics().status_code = 200
        result = self.handler.subscribe('em@il.com', ['code'])
        self.assertTrue(result)

    @mock.patch('data_research.handlers.settings')
    @mock.patch('data_research.handlers.messages')
    @mock.patch('data_research.handlers.GovDelivery')
    def test_subscribe_returns_False_for_nonset_account_code(self, mock_gd, mock_messages, mock_settings):
        mock_gd.side_effect = KeyError()
        result = self.handler.subscribe('em@il.com', ['code'])
        self.assertTrue(mock_messages.error.called)
        self.assertFalse(result)

    @mock.patch('data_research.handlers.settings')
    @mock.patch('data_research.handlers.messages')
    @mock.patch('data_research.handlers.GovDelivery')
    def test_subscribe_returns_False_when_setting_subscriptions(self, mock_gd, mock_messages, mock_settings):
        mock_gd().set_subscriber_topics.side_effect = Exception()
        result = self.handler.subscribe('em@il.com', ['code'])
        self.assertTrue(mock_messages.error.called)
        self.assertFalse(result)

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_sessions')
    @mock.patch('data_research.handlers.json')
    def test_save_attendee_calls_get_sessions(self, mock_json, mock_getsessions):
        attendee = mock.Mock()
        self.handler.save_attendee(attendee)
        self.assertTrue(mock_getsessions.called)

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_sessions')
    @mock.patch('data_research.handlers.json')
    def test_save_attendee_calls_json_dumps(self, mock_json, mock_getsessions):
        attendee = mock.Mock()
        self.handler.save_attendee(attendee)
        self.assertTrue(mock_json.dumps.called)

    @mock.patch('data_research.handlers.ConferenceRegistrationHandler.get_sessions')
    @mock.patch('data_research.handlers.json')
    def test_save_attendee_calls_save_on_attendee(self, mock_json, mock_getsessions):
        attendee = mock.Mock()
        self.handler.save_attendee(attendee)
        self.assertTrue(attendee.save.called)

    def test_get_sessions_returns_strings_from_block_value_if_in_post_data(self):
        self.handler.request = self.factory.post('/', {'form_sessions': ['0']})
        result = self.handler.get_sessions()
        self.assertEqual(result, ['Session 0 description'])

    @mock.patch('data_research.handlers.HttpResponseRedirect')
    @mock.patch('data_research.handlers.JsonResponse')
    @mock.patch('data_research.handlers.messages')
    def test_success_calls_JsonResponse_for_ajax(self, mock_messages, mock_json_response, mock_redirect):
        self.handler.request = self.factory.post('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.handler.success()
        mock_json_response.assert_called_with({'result': 'pass'})

    @mock.patch('data_research.handlers.HttpResponseRedirect')
    @mock.patch('data_research.handlers.JsonResponse')
    @mock.patch('data_research.handlers.messages')
    def test_sucess_returns_JsonResponse_for_ajax(self, mock_messages, mock_json_response, mock_redirect):
        self.handler.request = self.factory.post('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        result = self.handler.success()
        self.assertEqual(result, mock_json_response())

    @mock.patch('data_research.handlers.HttpResponseRedirect')
    @mock.patch('data_research.handlers.JsonResponse')
    @mock.patch('data_research.handlers.messages')
    def test_sucess_calls_messages_for_nonajax(self, mock_messages, mock_json_response, mock_redirect):
        self.handler.success()
        self.assertTrue(mock_messages.success.called)

    @mock.patch('data_research.handlers.HttpResponseRedirect')
    @mock.patch('data_research.handlers.JsonResponse')
    @mock.patch('data_research.handlers.messages')
    def test_sucess_returns_redirect_for_nonajax(self, mock_messages, mock_json_response, mock_redirect):
        self.handler.success()
        mock_redirect.assert_called_with(self.handler.page.url)

    @mock.patch('data_research.handlers.JsonResponse')
    @mock.patch('data_research.handlers.messages')
    def test_fail_calls_returns_JsonResponse_with_ajax_request(self, mock_messages, mock_json_response):
        form = mock.Mock()
        form.errors = {'err': ['error message']}
        self.handler.request = self.factory.get('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        result = self.handler.fail(form)
        mock_json_response.assert_called_with({'result': 'fail'})

    @mock.patch('data_research.handlers.JsonResponse')
    @mock.patch('data_research.handlers.messages')
    def test_fail_calls_returns_JsonResponse_with_ajax_request(self, mock_messages, mock_json_response):
        form = mock.Mock()
        form.errors = {'err': ['error message']}
        self.handler.fail(form)
        mock_messages.error.assert_called_with(self.handler.request, message='error message')
