from unittest import mock

# from django.apps import apps
# from django.http import Http404
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.utils import timezone

from teachers_digital_platform.views import (
    _grade_level_page, create_grade_level_page_handler, view_results
)


now = timezone.now()


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

    @mock.patch("teachers_digital_platform.views.SharedUrlForm")
    def test_view_results(self, mock_shared_url):
        test_request = self.factory.get(
            "/", HTTP_HOST="preview.localhost", SERVER_PORT=8000
        )
        with self.assertRaises(ValueError):
            response = view_results(test_request)
            self.assertEqual(response, 1)
            self.assertEqual(mock_shared_url.call_count, 1)
