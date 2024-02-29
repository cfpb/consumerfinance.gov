from django.test import SimpleTestCase, TestCase

from tccp.models import CardSurveyData

from .baker import baker


class CardSurveyDataTests(SimpleTestCase):
    def test_state_limitations_national(self):
        self.assertIsNone(
            CardSurveyData(
                availability_of_credit_card_plan="National"
            ).state_limitations
        )

    def test_state_limitations_single_state(self):
        self.assertEqual(
            CardSurveyData(
                availability_of_credit_card_plan="One State/Territory",
                state="NY",
            ).state_limitations,
            ["NY"],
        )

    def test_state_limitations_multiple_states(self):
        self.assertEqual(
            CardSurveyData(
                availability_of_credit_card_plan="Regional",
                state_multiple=["NJ", "NY"],
            ).state_limitations,
            ["NJ", "NY"],
        )


class CardSurveyDataQuerySetTests(TestCase):
    def test_available_in(self):
        for availability, state, state_multiple in [
            ("National", None, None),
            ("One State/Territory", "NY", None),
            ("Regional", None, "NJ; NY"),
        ]:
            baker.make(
                CardSurveyData,
                availability_of_credit_card_plan=availability,
                state=state,
                state_multiple=state_multiple,
            )

        qs = CardSurveyData.objects.all()

        self.assertEqual(qs.available_in(None).count(), 1)
        self.assertEqual(qs.available_in("NY").count(), 3)
        self.assertEqual(qs.available_in("NJ").count(), 2)
        self.assertEqual(qs.available_in("CT").count(), 1)

    def test_for_credit_tier(self):
        baker.make(
            CardSurveyData,
            targeted_credit_tiers=["Credit score 619 or less"],
            purchase_apr_poor=9.99,
            transfer_apr_poor=8.88,
            transfer_apr_min=7.77,
            transfer_apr_max=10.1,
        )

        baker.make(
            CardSurveyData,
            targeted_credit_tiers=["Credit score 619 or less"],
            purchase_apr_poor=None,
            transfer_apr_poor=None,
            transfer_apr_min=None,
            transfer_apr_max=None,
        )

        baker.make(
            CardSurveyData,
            targeted_credit_tiers=["Credit score of 720 or greater"],
            purchase_apr_great=9.99,
            transfer_apr_great=None,
            transfer_apr_min=7.77,
            transfer_apr_max=10.1,
        )

        qs_poor = CardSurveyData.objects.for_credit_tier(
            "Credit score 619 or less"
        )
        self.assertEqual(qs_poor.count(), 1)
        self.assertQuerysetEqual(
            qs_poor.values_list(
                "purchase_apr_for_tier",
                "transfer_apr_for_tier",
                "transfer_apr_for_ordering",
            ),
            [(9.99, 8.88, 8.88)],
        )

        qs_great = CardSurveyData.objects.for_credit_tier(
            "Credit score of 720 or greater"
        )
        self.assertEqual(qs_great.count(), 1)
        self.assertQuerysetEqual(
            qs_great.values_list(
                "purchase_apr_for_tier",
                "transfer_apr_for_tier",
                "transfer_apr_for_ordering",
            ),
            [(9.99, None, 7.77)],
        )
