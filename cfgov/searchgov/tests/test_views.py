from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from searchgov.views import (
    API_ENDPOINT,
    encode_url,
    get_affiliate,
    get_api_key,
)


class GetAffiliateTestCase(TestCase):
    @patch("searchgov.views.environment_is")
    def test_is_cfpb(self, test_patch):
        test_patch.return_value = False
        affiliate = get_affiliate({"current_language": "en"})
        self.assertEqual(affiliate, "cfpb")

    @patch("searchgov.views.environment_is")
    def test_is_cfpb_beta(self, test_patch):
        test_patch.return_value = True
        affiliate = get_affiliate({"current_language": "en"})
        self.assertEqual(affiliate, "cfpb_beta")

    @patch("searchgov.views.environment_is")
    def test_is_cfpb_es(self, test_patch):
        test_patch.return_value = False
        affiliate = get_affiliate({"current_language": "es"})
        self.assertEqual(affiliate, "cfpb_es")

    @patch("searchgov.views.environment_is")
    def test_is_cfpb_beta_es(self, test_patch):
        test_patch.return_value = True
        affiliate = get_affiliate({"current_language": "es"})
        self.assertEqual(affiliate, "cfpb_beta_es")


class GetApiKeyTestCase(TestCase):
    @patch.object(settings, "SEARCHGOV_API_KEY", "k")
    def test_english_key(self):
        self.assertEqual(get_api_key({"current_language": "en"}), "k")

    @patch.object(settings, "SEARCHGOV_ES_API_KEY", "x")
    def test_spanish_key(self):
        self.assertEqual(get_api_key({"current_language": "es"}), "x")


class EncodeUrlTestCase(TestCase):
    def test_encodes_non_url_safe_chars(self):
        self.assertEqual(
            encode_url({"query": "term&does=encode"}),
            API_ENDPOINT.format("query=term%26does%3Dencode"),
        )


class JsonTestCase(TestCase):
    def test_json_response(self):
        response = self.client.get("/search/?q=mortgage&format=json")
        self.assertEqual(response["Content-Type"], "application/json")

    def test_html_response(self):
        response = self.client.get("/search/?q=mortgage")
        self.assertEqual(response["Content-Type"], "text/html; charset=utf-8")
