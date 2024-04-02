from django.test import TestCase

from tccp.filterset import CardSurveyDataFilterSet
from tccp.models import CardSurveyData

from .baker import baker


class CardSurveyDataFilterSetTests(TestCase):
    def get_queryset(self):
        return CardSurveyData.objects.with_ratings()

    def test_filter_defaults_used_if_not_provided(self):
        self.assertEqual(
            CardSurveyDataFilterSet().data,
            {
                "ordering": "purchase_apr",
                "credit_tier": "Credit scores from 620 to 719",
            },
        )

    def test_field_value_used_if_specified(self):
        data = {
            "ordering": "purchase_apr",
            "credit_tier": "Credit score of 720 or greater",
        }
        self.assertEqual(CardSurveyDataFilterSet(data).data, data)

    def test_filter_by_situations_noop(self):
        baker.make(
            CardSurveyData,
            targeted_credit_tiers=["Credit scores from 620 to 719"],
            purchase_apr_good=0.99,
            _quantity=10,
        )

        qs = self.get_queryset()
        self.assertEqual(qs.count(), 10)

        fs = CardSurveyDataFilterSet(
            {"situations": ["Pay less interest"]}, queryset=qs
        )
        self.assertEqual(fs.qs.count(), 10)

    def test_filter_by_location(self):
        for state in ["NJ", "NY", "PA"]:
            baker.make(
                CardSurveyData,
                availability_of_credit_card_plan="One State/Territory",
                state=state,
                targeted_credit_tiers=["Credit scores from 620 to 719"],
                purchase_apr_good=0.99,
                _quantity=3,
            )

        qs = self.get_queryset()
        self.assertEqual(qs.count(), 9)

        fs = CardSurveyDataFilterSet({"location": "PA"}, queryset=qs)
        self.assertEqual(fs.qs.count(), 3)

    def test_filter_by_no_account_fee(self):
        baker.make(
            CardSurveyData,
            targeted_credit_tiers=["Credit scores from 620 to 719"],
            purchase_apr_good=0.99,
            periodic_fee_type=["Annual"],
        )

        qs = self.get_queryset()
        self.assertEqual(qs.count(), 1)

        fs = CardSurveyDataFilterSet({"no_account_fee": False}, queryset=qs)
        self.assertEqual(fs.qs.count(), 1)

        fs = CardSurveyDataFilterSet({"no_account_fee": True}, queryset=qs)
        self.assertEqual(fs.qs.count(), 0)

    def test_filter_by_rewards(self):
        baker.make(
            CardSurveyData,
            targeted_credit_tiers=["Credit scores from 620 to 719"],
            purchase_apr_good=0.99,
            rewards=["Cashback rewards"],
        )

        qs = self.get_queryset()
        self.assertEqual(qs.count(), 1)

        fs = CardSurveyDataFilterSet(
            {"rewards": ["Cashback rewards"]}, queryset=qs
        )
        self.assertEqual(fs.qs.count(), 1)

        fs = CardSurveyDataFilterSet(
            {"rewards": ["Other rewards"]}, queryset=qs
        )
        self.assertEqual(fs.qs.count(), 0)

        fs = CardSurveyDataFilterSet(
            {"rewards": ["Cashback rewards", "Other rewards"]}, queryset=qs
        )
        self.assertEqual(fs.qs.count(), 1)
