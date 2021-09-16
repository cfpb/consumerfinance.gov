from unittest.mock import Mock, patch

from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory, TestCase

from teachers_digital_platform.views import (
    _find_grade_selection_url, _grade_level_page, _handle_result_url,
    create_grade_level_page_handler, student_results, view_results
)


_time = 1623518461


class TestSurveyWizard(TestCase):

    def setUp(self):
        super(TestSurveyWizard, self).setUp()

        self.factory = RequestFactory()

    def test_create_grade_level_page_handler(self):
        response = create_grade_level_page_handler('3-5')
        assert callable(response)

    def test_grade_level_page(self):
        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )

        response = _grade_level_page(test_request, '3-5')
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

    @patch("teachers_digital_platform.views.SharedUrlForm")
    @patch("teachers_digital_platform.views._find_grade_selection_url")
    def test_invalid_results(self, mock_get_url, MockForm):
        MockForm.return_value.is_valid.return_value = False
        mock_get_url.return_value = "/grade-select"

        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )

        response = view_results(test_request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "/grade-select")

        response = student_results(test_request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "/grade-select")

    def test_invalid_method_results(self):
        test_request = self.factory.post(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )

        response = view_results(test_request)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 404)

        response = student_results(test_request)
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 404)

    @patch("teachers_digital_platform.views.SharedUrlForm")
    @patch("teachers_digital_platform.views._handle_result_url")
    def test_valid_results_defers_to_handle_result(
            self, mock_handle_result_url, MockForm):
        mock_handle_result_url.return_value = HttpResponse()

        instance = MockForm.return_value
        instance.cleaned_data = {
            "r": ("mock_signed_code", "mock_code")
        }
        instance.is_valid.return_value = True

        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )

        view_results(test_request)
        self.assertEqual(
            mock_handle_result_url.call_args[0],
            (test_request, 'mock_signed_code', 'mock_code', False)
        )

        test_request2 = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        test_request2.COOKIES = {"resultUrl": "cookie_code"}

        student_results(test_request2)

        self.assertEqual(MockForm.call_args[0], ({"r": "cookie_code"},))
        self.assertEqual(
            mock_handle_result_url.call_args[0],
            (test_request2, 'mock_signed_code', 'mock_code', True)
        )

    @patch("teachers_digital_platform.views.UrlEncoder")
    def test_handle_result_url(self, MockEncoder):
        instance = MockEncoder.return_value
        instance.loads.return_value = {
            "key": "3-5",
            "subtotals": [10, 10, 10],
            "time": _time
        }

        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )

        res = _handle_result_url(test_request, "signed", "code", True)
        self.assertEqual(instance.loads.call_args[0], ('code',))
        self.assertContains(res, 'data-signed-code="signed"')

    @patch("v1.models.SublandingPage")
    def test_find_grade_selection_url(self, MockSublandingPage):
        page_attrs = {'get_url.return_value': "/success"}
        page = Mock(**page_attrs)
        get = Mock(return_value=page)
        objects = Mock(get=get)
        MockSublandingPage.attach_mock(objects, 'objects')

        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        url = _find_grade_selection_url(
            test_request, 'default', MockSublandingPage)
        self.assertEqual(url, "/success")
