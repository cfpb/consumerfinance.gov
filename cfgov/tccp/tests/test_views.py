import json
from urllib.parse import quote_plus

from django.http import Http404
from django.shortcuts import reverse
from django.test import RequestFactory, TestCase

from django_htmx.middleware import HtmxMiddleware

from tccp.models import CardSurveyData
from tccp.views import CardDetailView, CardListView, LandingPageView

from .baker import baker


class LandingPageViewTests(TestCase):
    def make_request(self, querystring=""):
        view = LandingPageView.as_view()
        request = RequestFactory().get(f"/{querystring}")
        return view(request)

    def test_basic_get(self):
        response = self.make_request()
        self.assertEqual(response.status_code, 200)

    def test_situation_redirect(self):
        tier = "Credit scores from 620 to 719"

        response = self.make_request(
            "?location=NY"
            + "&credit_tier="
            + quote_plus(tier)
            + "&situations=Avoid+fees"
            + "&situations=Earn+rewards"
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            reverse("tccp:cards")
            + "?credit_tier="
            + quote_plus(tier)
            + "&location=NY"
            + "&situations=Avoid+fees"
            + "&situations=Earn+rewards"
            + "&ordering=purchase_apr"
            + "&no_account_fee=True"
            + "&rewards=Cashback+rewards"
            + "&rewards=Travel-related+rewards"
            + "&rewards=Other+rewards",
        )

    def test_invalid_query_still_renders_page(self):
        response = self.make_request("?credit_tier=foo")
        self.assertEqual(response.status_code, 200)


class AboutViewTests(TestCase):
    def test_get(self):
        response = self.client.get(reverse("tccp:about"))
        self.assertContains(response, "About this tool")


class CardListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(
            CardSurveyData,
            targeted_credit_tiers=["Credit score of 720 or greater"],
            purchase_apr_great=0.99,
            _quantity=5,
        )
        baker.make(
            CardSurveyData,
            _quantity=3,
        )

    def make_request(self, querystring="", **kwargs):
        view = HtmxMiddleware(CardListView.as_view())
        request = RequestFactory().get(f"/{querystring}", **kwargs)
        return view(request)

    def test_no_querystring_filters_by_good_tier(self):
        response = self.make_request()
        self.assertContains(response, "Consumer Financial Protection Bureau")
        self.assertContains(response, "There are no results for your search.")

    def test_invalid_situations(self):
        response = self.make_request("?situations=fake+and+bad")
        self.assertContains(response, "There are no results for your search.")

    def test_htmx_includes_only_results(self):
        response = self.make_request(**{"HTTP_HX-Request": "true"})
        self.assertNotContains(
            response, "Consumer Financial Protection Bureau"
        )
        self.assertContains(response, "There are no results for your search.")

    def test_filter_by_credit_score(self):
        response = self.make_request(
            "?credit_tier=Credit+score+of+720+or+greater"
        )
        self.assertContains(response, "5 results")

    def test_invalid_json_query_renders_error(self):
        response = self.make_request("?format=json&credit_tier=foo")
        self.assertEqual(response.status_code, 400)

        response.render()
        self.assertEqual(
            json.loads(response.content),
            {
                "credit_tier": [
                    (
                        "Select a valid choice. "
                        "foo is not one of the available choices."
                    )
                ]
            },
        )

    def test_invalid_html_query_renders_empty_page(self):
        response = self.make_request("?credit_tier=foo")
        self.assertContains(response, "There are no results for your search.")


class CardDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(
            CardSurveyData,
            slug="test-card",
            product_name="Test Card",
        )

    def make_request(self, slug, querystring=None):
        view = CardDetailView.as_view()
        request = RequestFactory().get(f"/{querystring}")
        return view(request, **{"slug": slug})

    def test_get(self):
        response = self.make_request("test-card")
        self.assertContains(response, "Test Card")
        self.assertContains(response, "m-breadcrumb")

    def test_get_format_json(self):
        response = self.make_request("test-card", "?format=json")
        response.render()

        self.assertEqual(response.status_code, 200)
        card = json.loads(response.content)
        self.assertEqual(card["card"]["product_name"], "Test Card")

    def test_get_invalid_uses_standard_404_handling(self):
        with self.assertRaises(Http404):
            self.make_request("invalid-card")

    def test_get_invalid_json(self):
        response = self.make_request("invalid-card", "?format=json")
        response.render()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.content),
            {"detail": "No CardSurveyData matches the given query."},
        )
