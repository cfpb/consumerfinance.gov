import json
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
    def get(self, path, accept=None):
        headers = {"accept": accept} if accept else {}
        return self.client.get(path, headers=headers)

    def test_well_known_probe_gets_empty_response(self):
        response = self.get("/.well-known/passkey-endpoints")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"")
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")

    def test_missing_static_file_gets_empty_response(self):
        response = self.get("/static/does-not-exist.css")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"")

    def test_json_client_gets_problem_details(self):
        response = self.get("/does not exist/", accept="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "application/problem+json")
        self.assertEqual(
            json.loads(response.content),
            {
                "type": "about:blank",
                "title": "Not Found",
                "status": 404,
                "instance": f"/does%20not%20exist/",
            },
        )

    def test_browser_gets_full_html_page(self):
        response = self.get("/does-not-exist/", accept=BROWSER_ACCEPT)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")
        self.assertContains(response, "404: Page not found", status_code=404)

    def test_wildcard_accept_gets_html(self):
        response = self.get("/does-not-exist/", accept="*/*")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")

    def test_text_client_gets_plain_text(self):
        response = self.get("/does-not-exist/", accept="text/plain")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")
        self.assertEqual(response.content, b"404 Not Found\n")

    def test_unsupported_accept_gets_plain_text(self):
        response = self.get(
            "/does-not-exist/", accept="application/vnd.unsupported"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "text/plain; charset=utf-8")

    def test_negotiated_responses_vary_on_accept(self):
        for accept in (BROWSER_ACCEPT, "application/json", "text/plain"):
            with self.subTest(accept=accept):
                response = self.get("/does-not-exist/", accept=accept)
                self.assertIn("Accept", response["Vary"])

    def test_content_404_still_gets_the_full_html_page(self):
        response = self.get(
            "/about-us/newsroom/does-not-exist/", accept=BROWSER_ACCEPT
        )
        self.assertContains(response, "404: Page not found", status_code=404)
