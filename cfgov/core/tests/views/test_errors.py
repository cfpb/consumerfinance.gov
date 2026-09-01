from unittest import mock

from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings

from core.views.errors import handle_error


class HandleErrorTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")

    def test_handle_error(self):
        with mock.patch(
            "core.views.errors.render", return_value=HttpResponse()
        ) as mock_render:
            handle_error(404, self.request)

        mock_render.assert_called_with(
            self.request,
            "v1/layouts/404.html",
            context={"request": self.request},
            status=404,
        )

    def test_error_while_handling_404_should_be_raised(self):
        with mock.patch(
            "core.views.errors.render", side_effect=RuntimeError
        ), self.assertRaises(RuntimeError):
            handle_error(404, self.request)

    def test_error_while_handling_500_should_log_plain_text_response(self):
        with mock.patch("core.views.errors.render", side_effect=RuntimeError):
            result = handle_error(500, self.request)
            self.assertIn(
                b"This request could not be processed", result.content
            )
            self.assertIn(b"HTTP Error 500.", result.content)


BROWSER_ACCEPT = (
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
)


@override_settings(DEBUG=False)
class ErrorHandlerTestCase(TestCase):
    def test_well_known_probe_gets_empty_response(self):
        response = self.client.get("/.well-known/passkey-endpoints")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"")
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")

    def test_missing_static_file_gets_empty_response(self):
        response = self.client.get("/static/does-not-exist.css")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"")

    def test_other_404s_get_full_html_page(self):
        response = self.client.get("/does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")
        self.assertContains(response, "404: Page not found", status_code=404)

    def test_content_404_still_gets_the_full_html_page(self):
        response = self.client.get("/about-us/newsroom/does-not-exist/")
        self.assertContains(response, "404: Page not found", status_code=404)
