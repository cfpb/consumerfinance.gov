from django.test import TestCase

from tccp.filterset import CardSurveyDataFilterSet
from tccp.models import CardSurveyData

from .baker import baker


class CardSurveyDataFilterSetTests(TestCase):
    def test_filter_defaults_used_if_not_provided(self):
        self.assertEqual(
            CardSurveyDataFilterSet().data,
            {
                "ordering": "purchase_apr",
                "targeted_credit_tiers": "Credit scores from 620 to 719",
            },
        )

    def test_field_value_used_if_specified(self):
        data = {
            "ordering": "purchase_apr",
            "targeted_credit_tiers": "Credit score of 720 or greater",
        }
        self.assertEqual(CardSurveyDataFilterSet(data).data, data)

    def test_filter_by_geo_availability(self):
        for state in ["NJ", "NY", "PA"]:
            baker.make(
                CardSurveyData,
                availability_of_credit_card_plan="One State/Territory",
                state=state,
                targeted_credit_tiers=["Credit scores from 620 to 719"],
                purchase_apr_good=0.99,
                _quantity=3,
            )

        qs = CardSurveyData.objects.all()
        self.assertEqual(qs.count(), 9)

        fs = CardSurveyDataFilterSet({"geo_availability": "PA"}, queryset=qs)
        self.assertEqual(fs.qs.count(), 3)

    def test_sorting_default_order_uses_purchase_apr(self):
        cards = [
            baker.make(
                CardSurveyData,
                targeted_credit_tiers=["Credit scores from 620 to 719"],
                purchase_apr_good=apr,
            )
            for apr in (0.5, 1, 0.25)
        ]

        qs = CardSurveyData.objects.all()
        fs = CardSurveyDataFilterSet(queryset=qs)
        self.assertQuerysetEqual(fs.qs, [cards[2], cards[0], cards[1]])

    def test_sorting_by_transfer_apr_and_other_tier(self):
        cards = [
            baker.make(
                CardSurveyData,
                targeted_credit_tiers=["Credit score of 720 or greater"],
                transfer_apr_great=apr,
            )
            for apr in (0.5, 1, 0.25)
        ]

        qs = CardSurveyData.objects.all()
        fs = CardSurveyDataFilterSet(
            {
                "targeted_credit_tiers": "Credit score of 720 or greater",
                "ordering": "transfer_apr",
            },
            queryset=qs,
        )
        self.assertQuerysetEqual(fs.qs, [cards[2], cards[0], cards[1]])

    def test_sorting_by_product_name(self):
        cards = [
            baker.make(
                CardSurveyData,
                product_name=product_name,
                targeted_credit_tiers=["Credit scores from 620 to 719"],
            )
            for product_name in ["e", "b", "a", "d", "c"]
        ]

        qs = CardSurveyData.objects.all()
        fs = CardSurveyDataFilterSet({"ordering": "product_name"}, queryset=qs)
        self.assertQuerysetEqual(
            fs.qs, [cards[2], cards[1], cards[4], cards[3], cards[0]]
        )
