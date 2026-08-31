import json
from unittest import mock

from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from core.govdelivery import MockGovDelivery
from core.views import (
    CacheTaggedTemplateView,
    TranslatedTemplateView,
    govdelivery_subscribe,
    handle_error,
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


class TranslatedTemplateViewTestCase(TestCase):
    def test_language_activation(self):
        request = RequestFactory().get("/")

        view = TranslatedTemplateView.as_view(template_name="test.html")
        response = view(request)
        self.assertEqual(response.context_data["current_language"], "en")

        view = TranslatedTemplateView.as_view(
            template_name="test.html", language="es"
        )
        response = view(request)
        self.assertEqual(response.context_data["current_language"], "es")


class CacheTaggedTemplateViewTestCase(TestCase):
    def test_cache_tag(self):
        request = RequestFactory().get("/")

        view = CacheTaggedTemplateView.as_view(
            template_name="test.html", cache_tag="test"
        )
        response = view(request)
        self.assertEqual(response["Edge-Cache-Tag"], "test")

    def test_no_cache_tag(self):
        request = RequestFactory().get("/")

        view = CacheTaggedTemplateView.as_view(
            template_name="test.html",
            cache_tag=None,
        )
        with self.assertRaises(ImproperlyConfigured):
            view(request)


class HandleErrorTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")

    def test_handle_error(self):
        with mock.patch("core.views.render") as mock_render:
            handle_error(404, self.request)

        mock_render.assert_called_with(
            self.request,
            "v1/layouts/404.html",
            context={"request": self.request},
            status=404,
        )

    def test_error_while_handling_404_should_be_raised(self):
        with mock.patch(
            "core.views.render", side_effect=RuntimeError
        ), self.assertRaises(RuntimeError):
            handle_error(404, self.request)

    def test_error_while_handling_500_should_log_plain_text_response(self):
        with mock.patch("core.views.render", side_effect=RuntimeError):
            result = handle_error(500, self.request)
            self.assertIn(
                b"This request could not be processed", result.content
            )
            self.assertIn(b"HTTP Error 500.", result.content)
