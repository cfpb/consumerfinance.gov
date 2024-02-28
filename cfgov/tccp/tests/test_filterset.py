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
