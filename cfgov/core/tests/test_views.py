import json
import sys
from mock import call, patch

if sys.version_info[0] < 3:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from django.test import TestCase
from django.core.urlresolvers import reverse


class GovDeliverySubscribeTest(TestCase):
    """
    This TestCase mocks the following:
    authenticated_session - removes the external govdelivery call
    set_subscriber_topics - removes another external govdelivery call
    assertEquals(urlparse(url).path, reverse(route_name)) was used over
    assertRedirects because the former doesn't require the templates to exist
    """

    def test_missing_email_address(self):
        response = self.client.post(reverse('govdelivery'),
                                    {'code': 'FAKE_CODE'})
        self.assertEquals(urlparse(response['Location']).path,
                          reverse('govdelivery:user_error'))

    def test_missing_gd_code(self):
        response = self.client.post(reverse('govdelivery'),
                                    {'email': 'fake@example.com'})
        self.assertEquals(urlparse(response['Location']).path,
                          reverse('govdelivery:user_error'))

    def test_missing_email_address_ajax(self):
        response = self.client.post(reverse('govdelivery'),
                                    {'code': 'FAKE_CODE'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content.decode('utf-8'),
                         json.dumps({'result': 'fail'}))

    def test_missing_gd_code_ajax(self):
        response = self.client.post(reverse('govdelivery'),
                                    {'code': 'FAKE_CODE'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content.decode('utf-8'),
                         json.dumps({'result': 'fail'}))

    @patch('govdelivery.api.authenticated_session')
    @patch('core.views.GovDelivery.set_subscriber_topics')
    def test_successful_subscribe(self, mock_gd, mock_auth_session):
        mock_gd.return_value.status_code = 200
        response = self.client.post(reverse('govdelivery'),
                                    {'code': 'FAKE_CODE',
                                     'email': 'fake@example.com'})
        mock_gd.assert_called_with('fake@example.com',
                                   ['FAKE_CODE'])
        self.assertEquals(urlparse(response['Location']).path,
                          reverse('govdelivery:success'))

    @patch('govdelivery.api.authenticated_session')
    @patch('core.views.GovDelivery.set_subscriber_topics')
    def test_successful_subscribe_ajax(self, mock_gd, mock_auth_session):
        mock_gd.return_value.status_code = 200
        response = self.client.post(reverse('govdelivery'),
                                    {'code': 'FAKE_CODE',
                                     'email': 'fake@example.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        mock_gd.assert_called_with('fake@example.com',
                                   ['FAKE_CODE'])
        self.assertEqual(response.content.decode('utf-8'),
                         json.dumps({'result': 'pass'}))

    @patch('govdelivery.api.authenticated_session')
    @patch('core.views.GovDelivery.set_subscriber_topics')
    def test_server_error(self, mock_gd, mock_auth_session):
        mock_gd.return_value.status_code = 500
        response = self.client.post(reverse('govdelivery'),
                                    {'code': 'FAKE_CODE',
                                     'email': 'fake@example.com'})
        mock_gd.assert_called_with('fake@example.com',
                                   ['FAKE_CODE'])
        self.assertEquals(urlparse(response['Location']).path,
                          reverse('govdelivery:server_error'))

    @patch('govdelivery.api.authenticated_session')
    @patch('core.views.GovDelivery.set_subscriber_topics')
    @patch('core.views.GovDelivery.set_subscriber_answers_to_question')
    def test_setting_subscriber_answers_to_questions(self,
                                                     mock_set_answers,
                                                     mock_set_topics,
                                                     mock_auth_session):
        mock_set_topics.return_value.status_code = 200
        response = self.client.post(reverse('govdelivery'),
                                    {'code': 'FAKE_CODE',
                                     'email': 'fake@example.com',
                                     'questionid_batman': 'robin',
                                     'questionid_hello': 'goodbye'})
        calls = [call('fake@example.com', 'batman', 'robin'),
                 call('fake@example.com', 'hello', 'goodbye')]
        mock_set_answers.assert_has_calls(calls, any_order=True)
        self.assertEqual(mock_set_answers.call_count, 2)

class RegsgovCommentTest(TestCase):
    def test_missing_comment_on(self):
        response = self.client.post(reverse('reg_comment'),
                                    {'general_comment': 'FAKE_COMMENT',
                                    'first_name': 'FAKE_FIRST',
                                    'last_name': 'FAKE_LAST'})
        self.assertEquals(urlparse(response['Location']).path,
                          reverse('reg_comment:user_error'))

    def test_missing_general_comment(self):
        response = self.client.post(reverse('reg_comment'),
                                    {'comment_on': 'FAKE_DOC_NUM',
                                    'first_name': 'FAKE_FIRST',
                                    'last_name': 'FAKE_LAST'})
        self.assertEquals(urlparse(response['Location']).path,
                          reverse('reg_comment:user_error'))

    def test_missing_first_name(self):
        response = self.client.post(reverse('reg_comment'),
                                    {'comment_on': 'FAKE_DOC_NUM',
                                    'general_comment': 'FAKE_COMMENT',
                                    'last_name': 'FAKE_LAST'})
        self.assertEquals(urlparse(response['Location']).path,
                          reverse('reg_comment:user_error'))

    def test_missing_last_name(self):
        response = self.client.post(reverse('reg_comment'),
                                    {'comment_on': 'FAKE_DOC_NUM',
                                    'general_comment': 'FAKE_COMMENT',
                                    'first_name': 'FAKE_FIRST'})
        self.assertEquals(urlparse(response['Location']).path,
                          reverse('reg_comment:user_error'))

    def test_missing_comment_on_ajax(self):
        response = self.client.post(reverse('reg_comment'),
                                    {'general_comment': 'FAKE_COMMENT',
                                    'first_name': 'FAKE_FIRST',
                                    'last_name': 'FAKE_LAST'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content.decode('utf-8'),
                         json.dumps({'result': 'fail'}))

    def test_missing_general_comment_ajax(self):
        response = self.client.post(reverse('reg_comment'),
                                    {'comment_on': 'FAKE_DOC_NUM',
                                    'first_name': 'FAKE_FIRST',
                                    'last_name': 'FAKE_LAST'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content.decode('utf-8'),
                         json.dumps({'result': 'fail'}))

    def test_missing_first_name_ajax(self):
        response = self.client.post(reverse('reg_comment'),
                                    {'comment_on': 'FAKE_DOC_NUM',
                                    'general_comment': 'FAKE_COMMENT',
                                    'last_name': 'FAKE_LAST'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content.decode('utf-8'),
                         json.dumps({'result': 'fail'}))


    def test_missing_last_name_ajax(self):
        response = self.client.post(reverse('reg_comment'),
                                    {'comment_on': 'FAKE_DOC_NUM',
                                    'general_comment': 'FAKE_COMMENT',
                                    'first_name': 'FAKE_FIRST'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.content.decode('utf-8'),
                         json.dumps({'result': 'fail'}))

    # @patch('core.views.submit_comment')
    # def test_successful_comment(self, mock_submit):
    #     mock_gd.return_value.status_code = 200
    #     response = self.client.post(reverse('reg_comment'),
    #                                 {'comment_on': 'FAKE_DOC_NUM',
    #                                 'general_comment': 'FAKE_COMMENT',
    #                                 'first_name': 'FAKE_FIRST',
    #                                 'last_name': 'FAKE_LAST'},
    #     mock_submit.assert_called_with('fake@example.com',
    #                                ['FAKE_CODE'])
    #     self.assertEquals(urlparse(response['Location']).path,
    #                       reverse('govdelivery:success'))