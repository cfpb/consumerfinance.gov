# -*- coding: utf-8 -*-
from unittest import mock

from django.test import RequestFactory, TestCase

from v1.handlers.blocks.feedback import FeedbackHandler, get_feedback_type
from v1.models import CFGOVPage, Feedback


class TestFeedbackHandler(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        page = mock.Mock()
        page.url = '/owning-a-home/'
        post_data = {
            'is_helpful': 1,
            'comment': 'Example comment.',
        }
        page.language = 'en'
        request = self.factory.post('/', post_data)
        self.handler = FeedbackHandler(
            page, request, block_value={'was_it_helpful_text': 1,
                                        'comment': 'Example comment.',
                                        'radio_intro': None}
        )

    def test_sanitize_non_ascii_referrer(self):
        """Make sure referrers with non-ascii characters are handled."""
        page = mock.Mock()
        page.url = '/es/obtener-respuestas/'
        page.language = 'es'
        non_ascii_referrer = (
            'https://www.consumerfinance.gov/es/obtener-respuestas/'
            'buscar-por-etiqueta/línea_de_crédito_personal/'
        )
        request = self.factory.get('/')
        request.META = {'HTTP_REFERER': non_ascii_referrer}
        handler = FeedbackHandler(page, request, block_value={})
        sanitized = handler.sanitize_referrer()
        self.assertIn('é', sanitized)

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.get_response')
    def test_process_calls_handler_get_response(self, mock_get_response):
        mock_get_response.return_value = "Success!"
        msg = self.handler.process(is_submitted=True)
        self.assertEqual(mock_get_response.call_count, 1)
        self.assertEqual(msg, "Success!")

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.get_response')
    @mock.patch('v1.handlers.blocks.feedback.FeedbackForm')
    def test_process_does_not_bind_form_non_submissions(
            self, mock_form, mock_get_response):
        self.handler.process(is_submitted=False)
        self.assertEqual(mock_get_response.call_count, 0)

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.get_response')
    def test_process_returns_get_response_call_for_submission(
        self, mock_get_response
    ):
        result = self.handler.process(True)
        self.assertEqual(result, mock_get_response())

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.fail')
    def test_get_response_calls_form_isvalid(self, mock_fail):
        form = mock.Mock()
        form.is_valid.return_value = False
        self.handler.get_response(form)
        self.assertTrue(form.is_valid.called)

    @mock.patch('v1.handlers.blocks.feedback.FeedbackHandler.fail')
    def test_get_response_calls_calls_fail_for_invalid_form(self, mock_fail):
        form = mock.Mock()
        form.is_valid.return_value = False
        self.handler.get_response(form)
        mock_fail.assert_called_with(form)

    @mock.patch('v1.handlers.blocks.feedback.HttpResponseRedirect')
    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_success_calls_JsonResponse_for_ajax(self,
                                                 mock_messages,
                                                 mock_json_response,
                                                 mock_redirect):
        self.handler.request = self.factory.post(
            '/', HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.handler.success()
        mock_json_response.assert_called_with(
            {'result': 'pass',
             'message': 'Thanks for your feedback!',
             'heading': ''}
        )

    @mock.patch('v1.handlers.blocks.feedback.HttpResponseRedirect')
    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_sucess_returns_JsonResponse_for_ajax(self,
                                                  mock_messages,
                                                  mock_json_response,
                                                  mock_redirect):
        self.handler.request = self.factory.post(
            '/', HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        result = self.handler.success()
        self.assertEqual(result, mock_json_response())

    @mock.patch('v1.handlers.blocks.feedback.HttpResponseRedirect')
    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_sucess_calls_messages_for_nonajax(self,
                                               mock_messages,
                                               mock_json_response,
                                               mock_redirect):
        self.handler.success()
        self.assertTrue(mock_messages.success.called)

    @mock.patch('v1.handlers.blocks.feedback.HttpResponseRedirect')
    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_sucess_returns_redirect_for_nonajax(self,
                                                 mock_messages,
                                                 mock_json_response,
                                                 mock_redirect):
        self.handler.success()
        mock_redirect.assert_called_with(self.handler.request.path)

    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_fail_calls_returns_JsonResponse_with_ajax_request(
        self,
        mock_messages,
        mock_json_response
    ):
        form = mock.Mock()
        self.handler.request = self.factory.get(
            '/', HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.handler.fail(form)

        mock_json_response.assert_called_with(
            {'result': 'fail',
             'message': 'You must select an option.'}
        )

    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_fail_calls_message_error_with_helpful_message_for_helpful_error(
        self, mock_messages, mock_json_response
    ):
        form = mock.Mock()
        form.errors.get.return_value = True
        self.handler.fail(form)
        mock_messages.error.assert_called_with(
            self.handler.request, 'You must select an option.'
        )

    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_fail_calls_message_error_with_other_message(self,
                                                         mock_messages,
                                                         mock_json_response):
        form = mock.Mock()
        form.errors.get.return_value = False
        self.handler.fail(form)
        mock_messages.error.assert_called_with(
            self.handler.request, 'Something went wrong. Please try again.'
        )

    @mock.patch('v1.handlers.blocks.feedback.JsonResponse')
    @mock.patch('v1.handlers.blocks.feedback.messages')
    def test_fail_calls_returns_form_dict(self,
                                          mock_messages,
                                          mock_json_response):
        form = mock.Mock()
        result = self.handler.fail(form)
        self.assertEqual(result, {'form': form})

    def test_get_feedback_type_helpful(self):
        block_value = {'was_it_helpful_text': 1,
                       'comment': 'Example comment.',
                       'radio_intro': None}
        self.assertEqual(get_feedback_type(block_value), 'helpful')

    def test_get_feedback_type_suggestion(self):
        block_value = {'was_it_helpful_text': None,
                       'comment': 'Example comment.',
                       'radio_intro': 'radio non-silence'}
        self.assertEqual(get_feedback_type(block_value), 'suggestion')

    def test_get_feedback_type_referred(self):
        block_value = {'was_it_helpful_text': None,
                       'comment': 'Example comment.',
                       'radio_intro': None}
        self.assertEqual(get_feedback_type(block_value), 'referred')

    def test_get_feedback_type_no_block_value(self):
        block_value = None
        self.assertEqual(get_feedback_type(block_value), 'helpful')

    def _post_feedback(self, page=None, referrer='None', is_helpful='None'):
        page = page or CFGOVPage.objects.first()

        post_data = {}
        if referrer is not None:
            post_data['referrer'] = referrer
        if is_helpful is not None:
            post_data['is_helpful'] = is_helpful

        request = self.factory.post(
            '/',
            post_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Create a block that will use the standard FeedbackForm.
        block_value = {'was_it_helpful_text': 'Was this helpful?'}
        handler = FeedbackHandler(page, request, block_value=block_value)
        response = handler.process(is_submitted=True)
        self.assertEqual(response.status_code, 200)

        return Feedback.objects.last()

    def test_page_gets_saved_with_feedback(self):
        page = CFGOVPage.objects.last()
        feedback = self._post_feedback(page=page)
        self.assertEqual(feedback.page.pk, page.pk)

    def test_is_helpful_gets_saved_with_feedback(self):
        feedback = self._post_feedback(is_helpful=True)
        self.assertTrue(feedback.is_helpful)

        feedback = self._post_feedback(is_helpful=False)
        self.assertFalse(feedback.is_helpful)

        feedback = self._post_feedback(is_helpful='None')
        self.assertIsNone(feedback.is_helpful)

    def test_referrer_gets_saved_with_feedback(self):
        feedback = self._post_feedback(referrer='foo')
        self.assertEqual(feedback.referrer, 'foo')

    def test_referrer_gets_truncated_if_excessively_long(self):
        feedback = self._post_feedback(referrer='x' * 1000)
        self.assertEqual(feedback.referrer, 'x' * 255)
