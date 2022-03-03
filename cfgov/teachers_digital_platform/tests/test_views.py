from unittest.mock import Mock, patch

from django.core import signing
from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory, TestCase

from teachers_digital_platform.UrlEncoder import UrlEncoder
from teachers_digital_platform.views import (
    SurveyWizard,
    _find_grade_selection_url,
    _grade_level_page,
    _handle_result_url,
    create_grade_level_page_handler,
    student_results,
    view_results,
)

_time = 1623518461


class TestSurveyWizard(TestCase):
    def setUp(self):
        super().setUp()

        self.factory = RequestFactory()

        key = "3-5"
        scores = [0, 10, 15]
        time = 1623518461
        self.code = UrlEncoder([key]).dumps(key, scores, time)
        self.signed_code = signing.Signer().sign(self.code)

    def test_create_grade_level_page_handler(self):
        response = create_grade_level_page_handler("3-5")
        assert callable(response)

    @patch("teachers_digital_platform.views.render_to_string")
    def test_grade_level_page(self, mock_rts):
        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        mock_rts.return_value = "success"
        response = _grade_level_page(test_request, "3-5")
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
        self, mock_handle_result_url, MockForm
    ):
        mock_handle_result_url.return_value = HttpResponse()

        instance = MockForm.return_value
        instance.cleaned_data = {"r": ("mock_signed_code", "mock_code")}
        instance.is_valid.return_value = True

        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )

        view_results(test_request)
        self.assertEqual(
            mock_handle_result_url.call_args[0],
            (test_request, "mock_signed_code", "mock_code", False),
        )

        test_request2 = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        test_request2.COOKIES = {"resultUrl": "cookie_code"}

        student_results(test_request2)

        self.assertEqual(MockForm.call_args[0], ({"r": "cookie_code"},))
        self.assertEqual(
            mock_handle_result_url.call_args[0],
            (test_request2, "mock_signed_code", "mock_code", True),
        )

    @patch("teachers_digital_platform.views.UrlEncoder")
    @patch("teachers_digital_platform.views.render_to_string")
    def test_handle_result_url(self, mock_rts, MockEncoder):
        instance = MockEncoder.return_value
        instance.loads.return_value = {
            "key": "3-5",
            "subtotals": [10, 10, 10],
            "time": _time,
        }

        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        mock_rts.return_value = 'data-signed-code="signed"'
        res = _handle_result_url(test_request, "signed", "code", True)
        self.assertEqual(instance.loads.call_args[0], ("code",))
        self.assertEqual(res.status_code, 200)

    @patch("v1.models.SublandingPage")
    def test_find_grade_selection_url(self, MockSublandingPage):
        page_attrs = {"get_url.return_value": "/success"}
        page = Mock(**page_attrs)
        get = Mock(return_value=page)
        objects = Mock(get=get)
        MockSublandingPage.attach_mock(objects, "objects")

        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        url = _find_grade_selection_url(
            test_request, "default", MockSublandingPage
        )
        self.assertEqual(url, "/success")

    def test_survey_wizard_build_views(self):
        sw = SurveyWizard()
        sw.survey_key = "3-5"
        wv = sw.build_views()
        keys = wv.keys()
        self.assertIn("3-5", keys)

    def test_student_results(self):
        test_request = self.factory.get(
            "/",
            {"r": self.signed_code},
            HTTP_HOST="preview.localhost",
            SERVER_PORT=8000,
        )
        test_request.COOKIES = {"resultUrl": "cookie_code"}
        response = student_results(test_request)
        self.assertEqual(response.status_code, 302)

    @patch("teachers_digital_platform.views.UrlEncoder.loads")
    def test_handle_result_url_redirect(self, mock_loads):
        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        mock_loads.return_value = None
        response = _handle_result_url(test_request, "signed", "code", True)
        self.assertEqual(response.status_code, 302)

    @patch("time.time")
    def test_survey_done_redirects_with_cookie(self, mock_time):
        mock_time.return_value = _time
        expected_code = "v1_3-5_10:z:h_1uo0"
        cleaned = {
            "q1": "0",
            "q2": "0",
            "q3": "0",
            "q4": "0",
            "q5": "0",
            "q6": "0",
            "q7": "0",
            "q8": "0",
            "q9": "0",
            "q10": "0",
            "q11": "0",
            "q12": "0",
            "q13": "0",
            "q14": "0",
            "q15": "0",
            "q16": "0",
            "q17": "0",
            "q18": "0",
            "q19": "0",
            "q20": "0",
        }
        mock_self = Mock()
        mock_self.get_all_cleaned_data.return_value = cleaned
        mock_self.survey_key = "3-5"
        response = SurveyWizard.done(mock_self, {})

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "../results/")
        cookie_val = response.cookies["resultUrl"].value
        code = signing.Signer().unsign(cookie_val)

        self.assertEqual(code, expected_code)
