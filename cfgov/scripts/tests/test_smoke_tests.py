"""Test the deployment http and static resource smoke tests."""
import unittest

import mock
import requests
from scripts import http_smoke_test, static_asset_smoke_test


class StaticAssetTests(unittest.TestCase):
    """Tests for the static assets smoke tests."""

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
    """Tests for the http smoke tests."""

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_get_full_list(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'top': ['url1'],
            'apps': ['url2']
        }
        mock_get.return_value = mock_response
        full_list = http_smoke_test.get_full_list()
        self.assertEqual(len(full_list), 2)
        self.assertEqual(mock_get.call_count, 1)

    @mock.patch('scripts.http_smoke_test.requests.get', side_effect=ValueError)
    def test_get_full_list_fallback(self, mock_get):
        """Check that script falls back to hard-coded list."""
        full_list = http_smoke_test.get_full_list()
        self.assertEqual(len(full_list), len(http_smoke_test.FULL_RUN))

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_http_success_url_list(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        http_smoke_test.check_urls('pro1', url_list=['/', '/ask-cfpb/'])
        self.assertEqual(
            mock_get.call_count,
            2
        )

    @mock.patch('scripts.http_smoke_test.requests.get')
    @mock.patch('scripts.http_smoke_test.get_full_list')
    def test_http_success_full(self, mock_list, mock_get):
        mock_list.return_value = http_smoke_test.FULL_RUN
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        http_smoke_test.check_urls('pro1')
        self.assertEqual(mock_get.call_count, len(http_smoke_test.FULL_RUN))

    @mock.patch('scripts.http_smoke_test.requests.get')
    def test_http_fail_url_list(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        mock_response.json.return_value = []
        result = http_smoke_test.check_urls('pro1', url_list='/')
        self.assertIs(result, False)
        self.assertEqual(mock_get.call_count, 1)

    @mock.patch('scripts.http_smoke_test.requests.get')
    @mock.patch('scripts.http_smoke_test.get_full_list')
    def test_http_fail_full(self, mock_list, mock_get):
        mock_response = mock.Mock()
        mock_list.return_value = http_smoke_test.FULL_RUN
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        result = http_smoke_test.check_urls('pro1')
        self.assertIs(result, False)
        self.assertEqual(mock_get.call_count, len(http_smoke_test.FULL_RUN))

    @mock.patch(
        'scripts.http_smoke_test.requests.get',
        side_effect=requests.exceptions.Timeout
    )
    def test_http_fail_timeout(self, mock_get):
        http_smoke_test.check_urls('pro1', url_list=['/'])
        self.assertEqual(mock_get.call_count, 1)

    @mock.patch(
        'scripts.http_smoke_test.requests.get',
        side_effect=requests.exceptions.Timeout
    )
    @mock.patch('scripts.http_smoke_test.get_full_list')
    def test_http_fail_timeout_full(self, mock_list, mock_get):
        mock_list.json.return_value = http_smoke_test.FULL_RUN
        http_smoke_test.check_urls('pro1')
        self.assertEqual(mock_get.call_count, 0)

    @mock.patch(
        'scripts.http_smoke_test.requests.get',
        side_effect=requests.exceptions.Timeout)
    def test_allowed_timeouts(self, mock_get):
        too_many = http_smoke_test.ALLOWED_TIMEOUTS + 2
        urls = http_smoke_test.FULL_RUN[:too_many]
        self.assertIs(
            http_smoke_test.check_urls('pro1', url_list=urls),
            False
        )

    @mock.patch(
        'scripts.http_smoke_test.requests.get',
        side_effect=requests.exceptions.ConnectionError
    )
    def test_http_fail_connection_error(self, mock_get):
        http_smoke_test.check_urls('pro1')
        self.assertEqual(
            mock_get.call_count,
            len(http_smoke_test.FULL_RUN) + 1  # one call for s3
        )

    @mock.patch(
        'scripts.http_smoke_test.requests.get',
        side_effect=requests.exceptions.RequestException
    )
    def test_http_fail_request_error(self, mock_get):
        result = http_smoke_test.check_urls('www', url_list=['/', '/ask-cfpb'])
        self.assertIs(result, False)
