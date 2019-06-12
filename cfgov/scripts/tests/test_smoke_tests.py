"""Test the dployment http and static resource smoke tests"""
import unittest

import mock
import requests
from scripts import http_smoke_test, static_asset_smoke_test


class StaticAssetTests(unittest.TestCase):
    """Tests for the static assets smoke tests"""

    mock_links = '<script type="text/javascript" src="/static/js/atomic/header.97504b419ce4.js"></script>\n\
                  <script type="text/javascript" src="static/js/atomic/header.97504b419ce4.js"></script>'  # noqa: E501

    @mock.patch('scripts.static_asset_smoke_test.requests.get')
    def test_home_page_test_success(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = self.mock_links
        mock_get.return_value = mock_response
        msg = static_asset_smoke_test.check_static('any-url.com/')
        self.assertEqual(mock_get.call_count, 3)
        self.assertIn('passed', msg)

    @mock.patch('scripts.static_asset_smoke_test.requests.get')
    def test_home_page_test_failure(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_response.content = self.mock_links
        mock_get.return_value = mock_response
        msg = static_asset_smoke_test.check_static('any-url.com/')
        self.assertEqual(mock_get.call_count, 3)
        self.assertIn('FAIL', msg)


class HttpTests(unittest.TestCase):
    """Tests for the http smoke tests"""

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_http_success_short(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        http_smoke_test.check_urls('pro1')
        self.assertEqual(mock_get.call_count, len(http_smoke_test.SHORT_RUN))

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_http_success_full(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        http_smoke_test.check_urls('pro1', full=True)
        self.assertEqual(mock_get.call_count,
                         len(http_smoke_test.SHORT_RUN +
                             http_smoke_test.FULL_RUN))

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_http_fail_short(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        http_smoke_test.check_urls('pro1')
        self.assertEqual(mock_get.call_count, len(http_smoke_test.SHORT_RUN))

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_http_fail_full(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        http_smoke_test.check_urls('pro1', full=True)
        self.assertEqual(mock_get.call_count,
                         len(http_smoke_test.SHORT_RUN +
                             http_smoke_test.FULL_RUN))

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_http_fail_timeout_short(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        http_smoke_test.check_urls('pro1')
        self.assertEqual(mock_get.call_count, len(http_smoke_test.SHORT_RUN))

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_http_fail_timeout_full(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        http_smoke_test.check_urls('pro1', full=True)
        self.assertEqual(mock_get.call_count,
                         len(http_smoke_test.SHORT_RUN +
                             http_smoke_test.FULL_RUN))

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_allowed_timeouts(self, mock_get):
        allowed = http_smoke_test.ALLOWED_TIMEOUTS
        mock_ok_response = mock.Mock()
        mock_ok_response.status_code = 200
        short_run_remainder = len(http_smoke_test.SHORT_RUN) - allowed
        allowed_list = [requests.exceptions.Timeout] * allowed
        ok_list = [mock_ok_response] * short_run_remainder
        side_effect_list = allowed_list + ok_list
        mock_get.side_effect = side_effect_list
        self.assertTrue(http_smoke_test.check_urls('pro1'))

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_http_fail_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError
        http_smoke_test.check_urls('pro1')
        self.assertEqual(mock_get.call_count, len(http_smoke_test.SHORT_RUN))

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_http_fail_request_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException
        http_smoke_test.check_urls('pro1')
        self.assertEqual(mock_get.call_count, len(http_smoke_test.SHORT_RUN))
