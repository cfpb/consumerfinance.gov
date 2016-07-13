import django
import json
import sys

from mock import Mock, call, patch

if sys.version_info[0] < 3:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

from urllib import urlencode
from django.test import RequestFactory, TestCase
from django.core.urlresolvers import reverse
from django.http import QueryDict

from django.contrib.messages.storage.cookie import CookieStorage
from django.contrib.messages import SUCCESS
from requests_toolbelt.multipart.encoder import MultipartEncoder

from core.utils import extract_answers_from_request
from core.views import govdelivery_subscribe, submit_comment


django.setup()


class GovDeliverySubscribeTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def post(self, post, ajax=False):
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'} if ajax else {}
        request = self.factory.post(reverse('govdelivery'), post, **kwargs)
        return govdelivery_subscribe(request)

    def assertRedirect(self, response, redirect):
        self.assertEqual(
            (response['Location'], response.status_code),
            (reverse(redirect), 302)
        )

    def assertRedirectSuccess(self, response):
        self.assertRedirect(response, 'govdelivery:success')

    def assertRedirectUserError(self, response):
        self.assertRedirect(response, 'govdelivery:user_error')

    def assertRedirectServerError(self, response):
        self.assertRedirect(response, 'govdelivery:server_error')

    def assertJSON(self, response, result):
        self.assertEqual(
            response.content.decode('utf-8'),
            json.dumps({'result': result})
        )

    def assertJSONSuccess(self, response):
        return self.assertJSON(response, 'pass')

    def assertJSONError(self, response):
        return self.assertJSON(response, 'fail')

    def mock_govdelivery(self, status_code=200):
        gd = Mock(set_subscriber_topics=Mock(
            return_value=Mock(status_code=status_code)
        ))

        patcher = patch('core.views.GovDelivery', return_value=gd)
        patched = patcher.start()
        self.addCleanup(patcher.stop)

        return gd

    def check_post(self, post, response_check, ajax=False):
        response_check(self.post(post, ajax=ajax))

    def test_missing_email_address(self):
        post = {'code': 'FAKE_CODE'}
        self.check_post(post, self.assertRedirectUserError)

    def test_missing_gd_code(self):
        post = {'email': 'fake@example.com'}
        self.check_post(post, self.assertRedirectUserError)

    def test_missing_email_address_ajax(self):
        post = {'code': 'FAKE_CODE'}
        self.check_post(post, self.assertJSONError, ajax=True)

    def test_missing_gd_code_ajax(self):
        post = {'email': 'fake@example.com'}
        self.check_post(post, self.assertJSONError, ajax=True)

    def check_subscribe(self, response_check, ajax=False, status_code=200,
                        include_answers=False):
        post = {
            'code': 'FAKE_CODE',
            'email': 'fake@example.com',
        }

        answers = [
            ('batman', 'robin'),
            ('hello', 'goodbye'),
        ]

        if include_answers:
            post.update({'questionid_' + q: a for q, a in answers})

        gd = self.mock_govdelivery(status_code=status_code)
        self.check_post(post, response_check, ajax=ajax)
        gd.set_subscriber_topics.assert_called_with(
            post['email'],
            [post['code']]
        )

        if include_answers:
            gd.set_subscriber_answers_to_question.assert_has_calls(
                [call(post['email'], q, a) for q, a in answers],
                any_order=True
            )

    def test_successful_subscribe(self):
        self.check_subscribe(self.assertRedirectSuccess)

    def test_successful_subscribe_ajax(self):
        self.check_subscribe(self.assertJSONSuccess, ajax=True)

    def test_server_error(self):
        self.check_subscribe(self.assertRedirectServerError, status_code=500)

    def test_server_error_ajax(self):
        self.check_subscribe(self.assertJSONError, ajax=True, status_code=500)

    def test_setting_subscriber_answers_to_questions(self):
        self.check_subscribe(self.assertRedirectSuccess, include_answers=True)


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
