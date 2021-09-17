import types

from unittest.mock import Mock, patch

from django.core import signing
from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory, TestCase

from teachers_digital_platform.UrlEncoder import UrlEncoder
from teachers_digital_platform.surveys import (
    AVAILABLE_SURVEYS
)
from teachers_digital_platform.views import (
    SurveyWizard, _find_grade_selection_url, _grade_level_page,
    _handle_result_url, create_grade_level_page_handler, student_results,
    view_results
)


_time = 1623518461


class TestSurveyWizard(TestCase):

    def setUp(self):
        super(TestSurveyWizard, self).setUp()

        self.factory = RequestFactory()

        key = '3-5'
        scores = [0, 10, 15]
        time = 1623518461
        self.code = UrlEncoder([key]).dumps(key, scores, time)
        self.signed_code = signing.Signer().sign(self.code)

    def test_create_grade_level_page_handler(self):
        response = create_grade_level_page_handler('3-5')
        assert callable(response)

    @patch('teachers_digital_platform.views.render_to_string')
    def test_grade_level_page(self, mock_rts):
        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        mock_rts.return_value = 'success'
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
    @patch('teachers_digital_platform.views.render_to_string')
    def test_handle_result_url(self, mock_rts, MockEncoder):
        instance = MockEncoder.return_value
        instance.loads.return_value = {
            "key": "3-5",
            "subtotals": [10, 10, 10],
            "time": _time
        }

        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        mock_rts.return_value = 'data-signed-code="signed"'
        res = _handle_result_url(test_request, "signed", "code", True)
        self.assertEqual(instance.loads.call_args[0], ('code',))
        self.assertEqual(res.status_code, 200)

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

    def test_survey_wizard_build_views(self):
        self.assertEqual(len(AVAILABLE_SURVEYS), 3)
        views = SurveyWizard().build_views()
        for key in AVAILABLE_SURVEYS:
            view = views[key]
            self.assertIs(view.view_class, SurveyWizard)
            self.assertIs(view.__class__, types.FunctionType)
            self.assertEqual(view.view_initkwargs['survey_key'], key)

    def test_student_results(self):
        test_request = self.factory.get(
            "/", {'r': self.signed_code},
            HTTP_HOST="preview.localhost",
            SERVER_PORT=8000
        )
        test_request.COOKIES = {'resultUrl': 'cookie_code'}
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

    def test_survey_done(self):
        view = SurveyWizard().build_views()['3-5']
        print(vars(view))
        print(vars(view.view_class))

        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        json = '{"step":"p5","step_data":{"p1":{"survey_wizard-current_step":["p1"],"p1-q1":["1"],"p1-q2":["1"],"p1-q3":["1"],"p1-q4":["1"],"p1-q5":["1"],"p1-q6":["1"]},"p2":{"survey_wizard-current_step":["p2"],"p2-q7":["0"],"p2-q8":["0"]},"p3":{"survey_wizard-current_step":["p3"],"p3-q9":["1"],"p3-q10":["1"],"p3-q11":["1"],"p3-q12":["1"],"p3-q13":["1"],"p3-q14":["1"],"p3-q15":["1"]},"p4":{"survey_wizard-current_step":["p4"],"p4-q16":["0"],"p4-q17":["0"],"p4-q18":["0"]},"p5":{"survey_wizard-current_step":["p5"],"p5-q19":["0"],"p5-q20":["0"]}},"step_files":{"p1":{},"p2":{},"p3":{},"p4":{},"p5":{}},"extra_data":{}}'
        test_request.COOKIES['wizard_survey_wizard'] = signing.get_cookie_signer().sign(json)

        response = view(test_request, step='done')
        # test redirects to "../results/"
        print(response)
