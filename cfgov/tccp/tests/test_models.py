from django.test import SimpleTestCase

from tccp.models import CardSurveyData


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
