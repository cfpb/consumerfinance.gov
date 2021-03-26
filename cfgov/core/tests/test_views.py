import json
import re
from unittest.mock import Mock, patch
from urllib.parse import urlencode

from django.http import Http404, QueryDict
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from requests_toolbelt.multipart.encoder import MultipartEncoder

from core.govdelivery import MockGovDelivery
from core.views import (
    ExternalURLNoticeView, TranslatedTemplateView, govdelivery_subscribe,
    regsgov_comment, submit_comment
)


class GovDeliverySubscribeTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def post(self, post, ajax=False):
        kwargs = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"} if ajax else {}
        request = self.factory.post(reverse("govdelivery"), post, **kwargs)
        return govdelivery_subscribe(request)

    def assertRedirect(self, response, redirect):
        self.assertEqual(
            (response["Location"], response.status_code),
            (reverse(redirect), 302),
        )

    def assertRedirectSuccess(self, response):
        self.assertRedirect(response, "govdelivery:success")

    def assertRedirectUserError(self, response):
        self.assertRedirect(response, "govdelivery:user_error")

    def assertRedirectServerError(self, response):
        self.assertRedirect(response, "govdelivery:server_error")

    def assertJSON(self, response, result):
        self.assertEqual(
            response.content.decode("utf-8"), json.dumps({"result": result})
        )

    def assertJSONSuccess(self, response):
        return self.assertJSON(response, "pass")

    def assertJSONError(self, response):
        return self.assertJSON(response, "fail")

    def check_post(self, post, response_check, ajax=False):
        response_check(self.post(post, ajax=ajax))

    def check_subscribe(
        self, response_check, ajax=False, include_answers=False
    ):
        post = {
            "code": "FAKE_CODE",
            "email": "fake@example.com",
        }

        answers = [
            ("batman", "robin"),
            ("hello", "goodbye"),
        ]

        if include_answers:
            post.update({"questionid_" + q: a for q, a in answers})

        self.check_post(post, response_check, ajax=ajax)

        self.assertEqual(
            MockGovDelivery.calls[0],
            (
                "set_subscriber_topics",
                (post["email"], [post["code"]]),
                {"send_notifications": True},
            ),
        )

        if include_answers:
            for i, (q, a) in enumerate(answers):
                self.assertEqual(
                    MockGovDelivery.calls[i + 1],
                    (
                        "set_subscriber_answers_to_question",
                        (post["email"], q, a),
                        {},
                    ),
                )

    def test_missing_email_address(self):
        post = {"code": "FAKE_CODE"}
        self.check_post(post, self.assertRedirectUserError)

    def test_missing_gd_code(self):
        post = {"email": "fake@example.com"}
        self.check_post(post, self.assertRedirectUserError)

    def test_missing_email_address_ajax(self):
        post = {"code": "FAKE_CODE"}
        self.check_post(post, self.assertJSONError, ajax=True)

    def test_missing_gd_code_ajax(self):
        post = {"email": "fake@example.com"}
        self.check_post(post, self.assertJSONError, ajax=True)

    def test_successful_subscribe(self):
        self.check_subscribe(self.assertRedirectSuccess)

    def test_successful_subscribe_ajax(self):
        self.check_subscribe(self.assertJSONSuccess, ajax=True)

    @override_settings(
        GOVDELIVERY_API="core.govdelivery.ExceptionMockGovDelivery"
    )
    def test_exception(self):
        self.check_subscribe(self.assertRedirectServerError)

    @override_settings(
        GOVDELIVERY_API="core.govdelivery.ExceptionMockGovDelivery"
    )
    def test_exception_ajax(self):
        self.check_subscribe(self.assertJSONError, ajax=True)

    @override_settings(
        GOVDELIVERY_API="core.govdelivery.ServerErrorMockGovDelivery"
    )
    def test_server_error(self):
        self.check_subscribe(self.assertRedirectServerError)

    @override_settings(
        GOVDELIVERY_API="core.govdelivery.ServerErrorMockGovDelivery"
    )
    def test_server_error_ajax(self):
        self.check_subscribe(self.assertJSONError, ajax=True)

    def test_setting_subscriber_answers_to_questions(self):
        self.check_subscribe(self.assertRedirectSuccess, include_answers=True)


class RegsgovCommentTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.data = {
            "comment_on": "FAKE_DOC_NUM",
            "general_comment": "FAKE_COMMENT",
            "first_name": "FAKE_FIRST",
            "last_name": "FAKE_LAST",
        }
        self.tracking_number = "FAKE_TRACKING_NUMBER"

    def post(self, post, ajax=False):
        kwargs = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"} if ajax else {}
        request = self.factory.post(reverse("reg_comment"), post, **kwargs)
        response = regsgov_comment(request)
        return request, response

    def assertRedirect(self, response, redirect):
        self.assertEqual(
            (response["Location"], response.status_code),
            (reverse(redirect), 302),
        )

    def assertRedirectSuccess(self, response):
        self.assertRedirect(response, "reg_comment:success")

    def assertRedirectUserError(self, response):
        self.assertRedirect(response, "reg_comment:user_error")

    def assertRedirectServerError(self, response):
        self.assertRedirect(response, "reg_comment:server_error")

    def assertJSON(self, response, result, has_tracking_num=False):
        expected = {"result": result}
        if has_tracking_num:
            expected.update({"tracking_number": self.tracking_number})

        self.assertEqual(
            response.content.decode("utf-8"), json.dumps(expected)
        )

    def assertJSONSuccessCommented(self, response):
        return self.assertJSON(response, "pass", has_tracking_num=True)

    def assertJSONError(self, response):
        return self.assertJSON(response, "fail")

    def check_post(self, post, response_check, ajax=False):
        request, response = self.post(post, ajax=ajax)
        response_check(response)
        return request, response

    def mock_submit_data(self, status_code=201):
        submit = Mock(
            status_code=status_code,
            text=json.dumps({"trackingNumber": self.tracking_number}),
        )

        patcher = patch("core.views.submit_comment", return_value=submit)
        patched = patcher.start()
        self.addCleanup(patcher.stop)
        return patched

    def mock_messages(self):
        patcher = patch("core.views.messages.success")
        patched = patcher.start()
        self.addCleanup(patcher.stop)
        return patched

    def check_comment(self, response_check, ajax=False, status_code=201):
        submit = self.mock_submit_data(status_code=status_code)
        messages = self.mock_messages()

        request, response = self.check_post(
            self.data, response_check, ajax=ajax
        )

        submit.assert_called_with(request.POST)

        if 201 == status_code:
            messages.assert_called_with(request, self.tracking_number)

    def test_missing_comment_on(self):
        del self.data["comment_on"]
        self.check_post(self.data, self.assertRedirectServerError)

    def test_missing_general_comment(self):
        del self.data["general_comment"]
        self.check_post(self.data, self.assertRedirectUserError)

    def test_missing_comment_on_ajax(self):
        del self.data["comment_on"]
        self.check_post(self.data, self.assertJSONError, ajax=True)

    def test_missing_general_comment_ajax(self):
        del self.data["general_comment"]
        self.check_post(self.data, self.assertJSONError, ajax=True)

    def test_missing_first_name_ajax(self):
        del self.data["first_name"]
        self.check_post(self.data, self.assertJSONError, ajax=True)

    def test_missing_last_name_ajax(self):
        del self.data["last_name"]
        self.check_post(self.data, self.assertJSONError, ajax=True)

    def test_successful_comment(self):
        self.check_comment(self.assertRedirectSuccess)

    def test_successful_comment_ajax(self):
        self.check_comment(self.assertJSONSuccessCommented, ajax=True)

    def test_server_error(self):
        self.check_comment(self.assertRedirectServerError, status_code=500)

    @patch("requests.post")
    @patch("django.conf.settings.REGSGOV_BASE_URL", "FAKE_URL")
    @patch("django.conf.settings.REGSGOV_API_KEY", "FAKE_API_KEY")
    def test_submit_comment_success_no_email(self, mock_post):
        mock_post.return_value = {"response": "fake_response"}

        data = {
            "comment_on": "FAKE_DOC_NUM",
            "general_comment": "FAKE_COMMENT",
            "first_name": "FAKE_FIRST",
            "last_name": "FAKE_LAST",
        }
        submit_comment(QueryDict(urlencode(data)))
        act_args, act_kwargs = mock_post.call_args

        self.assertEqual(
            act_args[0], "FAKE_URL?api_key=FAKE_API_KEY&D=FAKE_DOC_NUM"
        )
        exp_data_field = data
        exp_data_field["email"] = "NA"
        exp_data_field["organization"] = "NA"
        exp_data = MultipartEncoder(fields=exp_data_field)
        self.assertTrue(act_kwargs.get("data"), exp_data)
        self.assertEqual(act_kwargs.get("data").fields, exp_data.fields)
        self.assertIn("Content-Type", act_kwargs.get("headers"))

        self.assertIn(
            "multipart/form-data",
            act_kwargs.get("headers").get("Content-Type"),
        )

    @patch("requests.post")
    @patch("django.conf.settings.REGSGOV_BASE_URL", "FAKE_URL")
    @patch("django.conf.settings.REGSGOV_API_KEY", "FAKE_API_KEY")
    def test_submit_comment_success_email(self, mock_post):
        mock_post.return_value = {"response": "fake_response"}

        data = {
            "comment_on": "FAKE_DOC_NUM",
            "general_comment": "FAKE_COMMENT",
            "first_name": "FAKE_FIRST",
            "last_name": "FAKE_LAST",
            "email": "FAKE_EMAIL",
        }
        submit_comment(QueryDict(urlencode(data)))
        act_args, act_kwargs = mock_post.call_args

        self.assertEqual(
            act_args[0], "FAKE_URL?api_key=FAKE_API_KEY&D=FAKE_DOC_NUM"
        )
        exp_data_field = data
        exp_data_field["organization"] = "NA"
        exp_data = MultipartEncoder(fields=exp_data_field)
        self.assertTrue(act_kwargs.get("data"), exp_data)
        self.assertEqual(act_kwargs.get("data").fields, exp_data.fields)
        self.assertIn("Content-Type", act_kwargs.get("headers"))

        self.assertIn(
            "multipart/form-data",
            act_kwargs.get("headers").get("Content-Type"),
        )


class TestExternalURLNoticeView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        patched_whitelist = patch(
            "core.forms.EXTERNAL_URL_ALLOWLIST",
            (re.compile(r"^https:\/\/foo\.com$"),),
        )
        patched_whitelist.start()
        self.addCleanup(patched_whitelist.stop)

    def test_valid_get_returns_redirect(self):
        view = ExternalURLNoticeView.as_view()
        request = self.factory.get("/?ext_url=https://foo.com")
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_invalid_get_returns_404(self):
        view = ExternalURLNoticeView.as_view()
        request = self.factory.get("/?ext_url=https://bar.com")
        with self.assertRaises(Http404):
            view(request)


class TranslatedTemplateViewTestCase(TestCase):

    def test_language_activation(self):
        request = RequestFactory().get('/')

        view = TranslatedTemplateView.as_view(
            template_name='test.html'
        )
        response = view(request)
        self.assertEqual(response.context_data['current_language'], 'en')

        view = TranslatedTemplateView.as_view(
            template_name='test.html',
            language='es'
        )
        response = view(request)
        self.assertEqual(response.context_data['current_language'], 'es')
