from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import RequestFactory, TestCase, override_settings

from complaint_search import views as ComplaintViews
from rest_framework.response import Response

from legacy.views.complaint import ComplaintLandingView


class ComplaintLandingViewTests(TestCase):
    test_url = 'https://test.url/foo.json'

    def two_days_ago(self):
        return (datetime.now() - timedelta(2)).strftime("%Y-%m-%d")

    def setUp(self):
        self.request = RequestFactory().get('/')

    def assertNoBanner(self, response):
        self.assertNotContains(response, 'show-')

    @override_settings(COMPLAINT_LANDING_STATS_SOURCE=None)
    def test_no_stats_source(self):
        response = ComplaintLandingView.as_view()(self.request)
        self.assertNoBanner(response)

    @patch.object(ComplaintViews, 'search')
    def test_elasticsearch_down(self, mock_view):
        response = Response({})
        response.status = 404
        mock_view.return_value = response
        response = ComplaintLandingView.as_view()(self.request)
        self.assertTrue(mock_view.call_count == 1)
        self.assertNoBanner(response)

    @patch.object(ComplaintViews, 'search')
    def test_data_up_to_date(self, mock_view):
        data_json = {
            '_meta': {
                'last_indexed': self.two_days_ago(),
                'last_updated': self.two_days_ago(),
            },
        }
        response = Response(data_json)
        mock_view.return_value = response
        response = ComplaintLandingView.as_view()(self.request)
        self.assertTrue(mock_view.call_count == 1)
        self.assertNoBanner(response)

    @patch.object(ComplaintViews, 'search')
    def test_data_out_of_date(self, mock_view):
        data_json = {
            '_meta': {
                'last_indexed': '2010-01-01',
                'last_updated': self.two_days_ago(),
            }
        }
        response = Response(data_json)
        response.status = 200
        mock_view.return_value = response
        response = ComplaintLandingView.as_view()(self.request)
        self.assertTrue(mock_view.call_count == 1)
        self.assertContains(response, 'show-data-notification')

    @patch.object(ComplaintViews, 'search')
    def test_narratives_out_of_date(self, mock_view):
        data_json = {
            '_meta': {
                'last_indexed': self.two_days_ago(),
                'last_updated': '2010-01-01',
            },
        }
        response = Response(data_json)
        mock_view.return_value = response
        response.status = 200
        response = ComplaintLandingView.as_view()(self.request)
        self.assertTrue(mock_view.call_count == 1)
        self.assertContains(response, 'show-narratives-notification')

    @patch.object(ComplaintViews, 'search')
    def test_no_banner_when_data_invalid(self, mock_view):
        data_json = {
            'wrong_key': 5
        }
        response = Response(data_json)
        mock_view.return_value = response
        response = ComplaintLandingView.as_view()(self.request)
        self.assertTrue(mock_view.call_count == 1)
        self.assertNoBanner(response)

    @patch.object(ComplaintViews, 'search')
    def test_no_banner_when_data_not_json(self, mock_view):
        data_json = "not json"
        response = Response(data_json)
        mock_view.return_value = response
        response = ComplaintLandingView.as_view()(self.request)
        self.assertTrue(mock_view.call_count == 1)
        self.assertNoBanner(response)

    @patch.object(ComplaintViews, 'search')
    def test_no_banner_when_data_fetch_fails(self, mock_view):
        mock_view.return_value = Response('bleh')
        mock_view.side_effect = ValueError("test value error")
        response = ComplaintLandingView.as_view()(self.request)
        self.assertTrue(mock_view.call_count == 1)
        self.assertNoBanner(response)

    @patch.object(ComplaintViews, 'search')
    def test_no_banner_when_key_error(self, mock_view):
        mock_view.return_value = Response('bleh')
        mock_view.side_effect = KeyError("test key error")
        response = ComplaintLandingView.as_view()(self.request)
        self.assertTrue(mock_view.call_count == 1)
        self.assertNoBanner(response)
