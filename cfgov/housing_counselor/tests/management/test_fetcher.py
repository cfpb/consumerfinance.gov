from unittest import TestCase

import responses
from requests.exceptions import HTTPError

from housing_counselor.fetcher import (
    HUD_COUNSELORS_URL, HUD_LANGUAGES_URL, HUD_SERVICES_URL,
    download_housing_counselors, fetch_counselors, get_json_from_url,
    replace_abbreviations
)


class TestHousingCounselorFetcher(TestCase):
    @responses.activate
    def test_get_json_from_url_calls_requests_get(self):
        responses.add(responses.GET, 'http://test.url', json={'foo': 'bar'})
        response = get_json_from_url('http://test.url')
        self.assertEqual(response, {'foo': 'bar'})

    @responses.activate
    def test_get_json_from_url_raises_on_requests_failure(self):
        responses.add(responses.GET, 'http://test.url', status=503)
        with self.assertRaises(HTTPError):
            get_json_from_url('http://test.url')

    @responses.activate
    def test_replace_abbrevations_replaces_abbreviations(self):
        counselors = [
            {'foo': 'a,b', 'bar': 'x'},
            {'foo': 'b,c', 'bar': 'y'},
            {'foo': None, 'bar': None},
        ]

        url = 'http://test.url'
        responses.add(responses.GET, url, json=[
            {'key': 'a', 'value': 'apple'},
            {'key': 'b', 'value': 'blueberry'},
            {'key': 'c', 'value': 'coconut'},
        ])

        replace_abbreviations(counselors, 'foo', url)

        self.assertEqual(counselors, [
            {'foo': ['apple', 'blueberry'], 'bar': 'x'},
            {'foo': ['blueberry', 'coconut'], 'bar': 'y'},
            {'foo': [], 'bar': None},
        ])

    @responses.activate
    def test_no_housing_counselors_raises_exception(self):
        url = 'http://test.url'
        responses.add(responses.GET, url, body='[]')
        with self.assertRaises(RuntimeError):
            download_housing_counselors(url)

    @responses.activate
    def test_fetch(self):
        responses.add(
            responses.GET,
            HUD_COUNSELORS_URL,
            match_querystring=True,
            json=[{'foo': 'bar', 'languages': 'a,b', 'services': 'y,z'}]
        )

        responses.add(
            responses.GET,
            HUD_LANGUAGES_URL,
            json=[
                {'key': 'a', 'value': 'apple'},
                {'key': 'b', 'value': 'banana'},
            ]
        )

        responses.add(
            responses.GET,
            HUD_SERVICES_URL,
            json=[
                {'key': 'y', 'value': 'yam'},
                {'key': 'z', 'value': 'zzzzzz'},
            ]
        )

        self.assertEqual(fetch_counselors(), [
            {
                'foo': 'bar',
                'languages': ['apple', 'banana'],
                'services': ['yam', 'zzzzzz'],
            }
        ])
