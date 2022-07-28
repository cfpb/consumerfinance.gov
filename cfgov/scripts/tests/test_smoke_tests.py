"""Test the deployment http and static resource smoke tests."""
import unittest
from unittest import mock

import requests

from scripts import static_asset_smoke_test
from scripts.http_smoke_test import (
    ALLOWED_TIMEOUTS,
    FALLBACK_URLS,
    check_urls,
    get_full_list,
)


class StaticAssetTests(unittest.TestCase):
    """Tests for the static assets smoke tests."""

    mock_links = '<script src="/static/js/atomic/header.97504b419ce4.js"></script>\n\
                  <script src="static/js/atomic/header.97504b419ce4.js"></script>'  # noqa: B950

    @mock.patch("scripts.static_asset_smoke_test.requests.get")
    def test_home_page_test_success(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = self.mock_links
        mock_get.return_value = mock_response
        msg = static_asset_smoke_test.check_static("/any-url.com/")
        self.assertEqual(mock_get.call_count, 3)
        self.assertIn("passed", msg)

    @mock.patch("scripts.static_asset_smoke_test.requests.get")
    def test_home_page_test_partial_failure(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_response.content = self.mock_links
        mock_get.return_value = mock_response
        msg = static_asset_smoke_test.check_static("/sub-url-1/ /sub_url-2/")
        self.assertEqual(mock_get.call_count, 3)
        self.assertIn("Partial", msg)

    @mock.patch("scripts.static_asset_smoke_test.requests.get")
    def test_request_failure(self, mock_get):
        mock_response = mock.Mock()
        mock_response.ok = False
        mock_get.return_value = mock_response
        msg = static_asset_smoke_test.check_static("/mock-url/")
        self.assertIn("FAIL", msg)

    @mock.patch("scripts.static_asset_smoke_test.requests.get")
    @mock.patch("scripts.static_asset_smoke_test.extract_static_links")
    def test_link_check_failure(self, mock_extract, mock_get):
        mock_extract.return_value = ["mock_link", "mock_link", "mock_link"]
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        msg = static_asset_smoke_test.check_static("/mock_url/")
        self.assertIn("FAIL", msg)


class HttpTests(unittest.TestCase):
    """Tests for the http smoke tests."""

    @mock.patch("scripts.http_smoke_test.requests.get")
    def test_get_full_list(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {"top": ["url1"], "apps": ["url2"]}
        mock_get.return_value = mock_response
        full_list = get_full_list()
        self.assertEqual(len(full_list), 2)
        self.assertEqual(mock_get.call_count, 1)

    @mock.patch("scripts.http_smoke_test.requests.get", side_effect=ValueError)
    def test_get_full_list_fallback(self, mock_get):
        """Check that script falls back to hard-coded list."""
        full_list = get_full_list()
        self.assertEqual(len(full_list), len(FALLBACK_URLS))

    @mock.patch("scripts.http_smoke_test.requests.get")
    def test_http_success_url_list(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(check_urls("pro1", url_list=["/", "/ask-cfpb/"]))
        self.assertEqual(mock_get.call_count, 2)

    @mock.patch("scripts.http_smoke_test.requests.get")
    @mock.patch("scripts.http_smoke_test.get_full_list")
    def test_http_success_full(self, mock_list, mock_get):
        mock_list.return_value = FALLBACK_URLS
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(check_urls("pro1"))
        self.assertEqual(mock_get.call_count, len(FALLBACK_URLS))

    @mock.patch("scripts.http_smoke_test.requests.get")
    def test_http_fail_url_list(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        mock_response.json.return_value = []
        result = check_urls("pro1", url_list="/")
        self.assertFalse(result)
        self.assertEqual(mock_get.call_count, 1)

    @mock.patch("scripts.http_smoke_test.requests.get")
    @mock.patch("scripts.http_smoke_test.get_full_list")
    def test_http_fail_full(self, mock_list, mock_get):
        mock_response = mock.Mock()
        mock_list.return_value = FALLBACK_URLS
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        result = check_urls("pro1")
        self.assertFalse(result)
        self.assertEqual(mock_get.call_count, len(FALLBACK_URLS))

    @mock.patch(
        "scripts.http_smoke_test.requests.get",
        side_effect=requests.exceptions.Timeout,
    )
    def test_http_fail_timeout(self, mock_get):
        check_urls("pro1", url_list=["/"])
        self.assertEqual(mock_get.call_count, 1)

    @mock.patch(
        "scripts.http_smoke_test.requests.get",
        side_effect=requests.exceptions.Timeout,
    )
    def test_http_fail_timeout_full(self, mock_get):
        expected_call_count = len(FALLBACK_URLS) + 1  # one call for s3
        self.assertFalse(check_urls("pro1"))
        self.assertEqual(mock_get.call_count, expected_call_count)

    @mock.patch(
        "scripts.http_smoke_test.requests.get",
        side_effect=requests.exceptions.Timeout,
    )
    def test_allowed_timeouts(self, mock_get):
        too_many = ALLOWED_TIMEOUTS + 2
        urls = FALLBACK_URLS[:too_many]
        self.assertFalse(check_urls("pro1", url_list=urls))

    @mock.patch(
        "scripts.http_smoke_test.requests.get",
        side_effect=requests.exceptions.ConnectionError,
    )
    def test_http_fail_connection_error(self, mock_get):
        check_urls("pro1")
        self.assertEqual(
            mock_get.call_count, len(FALLBACK_URLS) + 1
        )  # one call for s3

    @mock.patch(
        "scripts.http_smoke_test.requests.get",
        side_effect=requests.exceptions.RequestException,
    )
    def test_http_fail_request_error(self, mock_get):
        result = check_urls("www", url_list=["/", "/ask-cfpb"])
        self.assertFalse(result)
