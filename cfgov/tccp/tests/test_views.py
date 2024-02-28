import json
from urllib.parse import quote_plus

from django.shortcuts import reverse
from django.test import RequestFactory, TestCase

from tccp.enums import CreditTierChoices
from tccp.models import CardSurveyData
from tccp.views import CardListView, LandingPageView

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
        tier = CreditTierChoices[2][0]

        response = self.make_request(
            "?credit_tier="
            + quote_plus(tier)
            + "&situation=Have+a+lower+monthly+payment"
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            reverse("tccp:cards")
            + "?targeted_credit_tiers="
            + quote_plus(tier)
            + "&ordering=purchase_apr",
        )

    def test_invalid_query_still_renders_page(self):
        response = self.make_request("?credit_tier=foo")
        self.assertEqual(response.status_code, 200)


class CardListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        baker.make(
            CardSurveyData,
            targeted_credit_tiers="Credit score of 720 or greater",
            purchase_apr_great=0.99,
            _quantity=5,
        )
        baker.make(
            CardSurveyData,
            targeted_credit_tiers="No credit score",
            _quantity=3,
        )

    def make_request(self, querystring=""):
        view = CardListView.as_view()
        request = RequestFactory().get(f"/{querystring}")
        return view(request)

    def test_no_querystring_filters_by_good_tier(self):
        response = self.make_request()
        self.assertContains(response, "There are no results for your search.")

    def test_filter_by_no_credit_score(self):
        response = self.make_request(
            "?targeted_credit_tiers=Credit+score+of+720+or+greater"
        )
        self.assertContains(response, "5 results")

    def test_invalid_json_query_renders_error(self):
        response = self.make_request("?format=json&targeted_credit_tiers=foo")
        self.assertEqual(response.status_code, 400)

        response.render()
        self.assertEqual(
            json.loads(response.content),
            {
                "targeted_credit_tiers": [
                    "Select a valid choice. foo is not one of the available choices."
                ]
            },
        )

    def test_invalid_html_query_renders_empty_page(self):
        response = self.make_request("?targeted_credit_tiers=foo")
        self.assertContains(response, "There are no results for your search.")
