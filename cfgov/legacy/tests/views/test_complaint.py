from datetime import datetime, timedelta

from django.test import RequestFactory, TestCase, override_settings

import responses
from requests.exceptions import RequestException

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

    @responses.activate
    @override_settings(COMPLAINT_LANDING_STATS_SOURCE=test_url)
    def test_data_up_to_date(self):
        data_json = {
            '_meta': {
                'last_indexed': self.two_days_ago(),
                'last_updated': self.two_days_ago(),
            },
        }
        responses.add(responses.GET, self.test_url, json=data_json)
        response = ComplaintLandingView.as_view()(self.request)
        self.assertNoBanner(response)

    @responses.activate
    @override_settings(COMPLAINT_LANDING_STATS_SOURCE=test_url)
    def test_data_out_of_date(self):
        data_json = {
            '_meta': {
                'last_indexed': '2010-01-01',
                'last_updated': self.two_days_ago(),
            },
        }
        responses.add(responses.GET, self.test_url, json=data_json)
        response = ComplaintLandingView.as_view()(self.request)
        self.assertContains(response, 'show-data-notification')

    @responses.activate
    @override_settings(COMPLAINT_LANDING_STATS_SOURCE=test_url)
    def test_narratives_out_of_date(self):
        data_json = {
            '_meta': {
                'last_indexed': self.two_days_ago(),
                'last_updated': '2010-01-01',
            },
        }
        responses.add(responses.GET, self.test_url, json=data_json)
        response = ComplaintLandingView.as_view()(self.request)
        self.assertContains(response, 'show-narratives-notification')

    @responses.activate
    @override_settings(COMPLAINT_LANDING_STATS_SOURCE=test_url)
    def test_no_banner_when_data_invalid(self):
        data_json = {
            'wrong_key': 5
        }
        responses.add(responses.GET, self.test_url, json=data_json)
        response = ComplaintLandingView.as_view()(self.request)
        self.assertNoBanner(response)

    @responses.activate
    @override_settings(COMPLAINT_LANDING_STATS_SOURCE=test_url)
    def test_no_banner_when_data_not_json(self):
        responses.add(responses.GET, self.test_url, body="not json")
        response = ComplaintLandingView.as_view()(self.request)
        self.assertNoBanner(response)

    @responses.activate
    @override_settings(COMPLAINT_LANDING_STATS_SOURCE=test_url)
    def test_no_banner_when_data_fetch_fails(self):
        responses.add(
            responses.GET,
            self.test_url,
            body=RequestException("test")
        )
        response = ComplaintLandingView.as_view()(self.request)
        self.assertNoBanner(response)
