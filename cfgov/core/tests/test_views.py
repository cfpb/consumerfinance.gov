import json
import sys

from mock import call, patch

if sys.version_info[0] < 3:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from urllib import urlencode
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.http import QueryDict

from django.contrib.messages.storage.cookie import CookieStorage
from django.contrib.messages import SUCCESS
from requests_toolbelt.multipart.encoder import MultipartEncoder
from core.views import submit_comment


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
                          reverse('reg_comment:server_error'))

    def test_missing_general_comment(self):
        response = self.client.post(reverse('reg_comment'),
                                    {'comment_on': 'FAKE_DOC_NUM',
                                    'first_name': 'FAKE_FIRST',
                                    'last_name': 'FAKE_LAST'})
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

    @patch('core.views.submit_comment')
    def test_successful_comment(self, mock_submit):
        mock_submit.return_value.status_code = 201
        mock_submit.return_value.text = '{"trackingNumber": "FAKE_TRACK_NUM"}'
        data = {'comment_on': 'FAKE_DOC_NUM',
                'general_comment': 'FAKE_COMMENT',
                'first_name': 'FAKE_FIRST',
                'last_name': 'FAKE_LAST'}
        response = self.client.post(reverse('reg_comment'), data)

        mock_submit.assert_called_with(QueryDict(urlencode(data)))
        self.assertEquals(urlparse(response['Location']).path,
                          reverse('reg_comment:success'))
        # TODO: There may be a better way to get messages_list,
        # fix if possible
        messages_list = CookieStorage(response)._decode(
                            response.cookies['messages'].value)
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, 'FAKE_TRACK_NUM')
        self.assertEqual(messages_list[0].level, SUCCESS)

    @patch('core.views.submit_comment')
    def test_successful_comment_ajax(self, mock_submit):
        mock_submit.return_value.status_code = 201
        mock_submit.return_value.text = '{"trackingNumber": "FAKE_TRACK_NUM"}'
        data = {'comment_on': 'FAKE_DOC_NUM',
                'general_comment': 'FAKE_COMMENT',
                'first_name': 'FAKE_FIRST',
                'last_name': 'FAKE_LAST'}
        response = self.client.post(reverse('reg_comment'), data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        mock_submit.assert_called_with(QueryDict(urlencode(data)))
        self.assertEqual(response.content.decode('utf-8'),
                         json.dumps({'result': 'pass', 'tracking_number': 'FAKE_TRACK_NUM'}))


    @patch('core.views.submit_comment')
    def test_server_error(self, mock_submit):
        mock_submit.return_value.status_code = 500
        data = {'comment_on': 'FAKE_DOC_NUM',
                'general_comment': 'FAKE_COMMENT',
                'first_name': 'FAKE_FIRST',
                'last_name': 'FAKE_LAST'}
        response = self.client.post(reverse('reg_comment'), data)

        mock_submit.assert_called_with(QueryDict(urlencode(data)))
        self.assertEquals(urlparse(response['Location']).path,
                          reverse('reg_comment:server_error'))


    # Test that throws an exception to go to server server_error

    # Test to submit comment

    @patch('requests.post')
    @patch('django.conf.settings.REGSGOV_BASE_URL', 'FAKE_URL')
    @patch('django.conf.settings.REGSGOV_API_KEY', 'FAKE_API_KEY')
    def test_submit_comment_success_no_email(self, mock_post):
        mock_post.return_value = {'response': 'fake_response'}

        data = {'comment_on': u'FAKE_DOC_NUM',
                'general_comment': u'FAKE_COMMENT',
                'first_name': u'FAKE_FIRST',
                'last_name': u'FAKE_LAST'}
        response = submit_comment(QueryDict(urlencode(data)))
        act_args, act_kwargs = mock_post.call_args

        self.assertEqual(act_args[0], 'FAKE_URL?api_key=FAKE_API_KEY&D=FAKE_DOC_NUM')
        exp_data_field = data
        exp_data_field['email'] = u'NA'
        exp_data_field['organization'] = u'NA'
        exp_data = MultipartEncoder(fields=exp_data_field)
        self.assertTrue(act_kwargs.get('data'), exp_data)
        self.assertEqual(act_kwargs.get('data').fields, exp_data.fields)
        self.assertTrue(act_kwargs.get('headers').has_key('Content-Type'))

        self.assertIn('multipart/form-data', act_kwargs.get('headers').get('Content-Type'))

    @patch('requests.post')
    @patch('django.conf.settings.REGSGOV_BASE_URL', 'FAKE_URL')
    @patch('django.conf.settings.REGSGOV_API_KEY', 'FAKE_API_KEY')
    def test_submit_comment_success_email(self, mock_post):
        mock_post.return_value = {'response': 'fake_response'}

        data = {'comment_on': u'FAKE_DOC_NUM',
                'general_comment': u'FAKE_COMMENT',
                'first_name': u'FAKE_FIRST',
                'last_name': u'FAKE_LAST',
                'email': u'FAKE_EMAIL'}
        response = submit_comment(QueryDict(urlencode(data)))
        act_args, act_kwargs = mock_post.call_args

        self.assertEqual(act_args[0], 'FAKE_URL?api_key=FAKE_API_KEY&D=FAKE_DOC_NUM')
        exp_data_field = data
        exp_data_field['organization'] = u'NA'
        exp_data = MultipartEncoder(fields=exp_data_field)
        self.assertTrue(act_kwargs.get('data'), exp_data)
        self.assertEqual(act_kwargs.get('data').fields, exp_data.fields)
        self.assertTrue(act_kwargs.get('headers').has_key('Content-Type'))

        self.assertIn('multipart/form-data', act_kwargs.get('headers').get('Content-Type'))
