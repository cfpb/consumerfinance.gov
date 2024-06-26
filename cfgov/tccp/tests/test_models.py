from datetime import date
from itertools import product

from django.test import SimpleTestCase, TestCase

from tccp.enums import (
    CreditTierColumns,
    LateFeeTypeChoices,
    OverlimitFeeTypeChoices,
)
from tccp.models import CardSurveyData

from .baker import baker


class CardSurveyDataQuerySetTests(TestCase):
    def get_queryset(self):
        return CardSurveyData.objects.with_ratings()

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

        qs = self.get_queryset()

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

        qs_poor = self.get_queryset().for_credit_tier(
            "Credit score 619 or less"
        )
        self.assertEqual(qs_poor.count(), 1)
        self.assertQuerysetEqual(
            qs_poor.values_list(
                "purchase_apr_for_tier_max",
                "purchase_apr_for_tier_rating",
                "transfer_apr_for_tier_max",
            ),
            [(9.99, 2, 8.88)],
        )

        qs_great = self.get_queryset().for_credit_tier(
            "Credit score of 720 or greater"
        )
        self.assertEqual(qs_great.count(), 1)
        self.assertQuerysetEqual(
            qs_great.values_list(
                "purchase_apr_for_tier_max",
                "purchase_apr_for_tier_rating",
                "transfer_apr_for_tier_max",
            ),
            [(9.99, 2, 10.1)],
        )

    def test_get_summary_statistics(self):
        today = date(2024, 12, 31)

        baker.make(
            CardSurveyData,
            report_date=today,
            targeted_credit_tiers=[
                "Credit score 619 or less",
                "Credit scores from 620 to 719",
                "Credit score of 720 or greater",
            ],
            purchase_apr_poor=3,
            purchase_apr_good=2,
            purchase_apr_great=1,
        )

        baker.make(
            CardSurveyData,
            report_date=today,
            targeted_credit_tiers=[
                "Credit score 619 or less",
                "Credit scores from 620 to 719",
                "Credit score of 720 or greater",
            ],
            purchase_apr_poor=9,
            purchase_apr_good=6,
            purchase_apr_great=3,
        )

        baker.make(
            CardSurveyData,
            report_date=today,
            targeted_credit_tiers=[
                "Credit score 619 or less",
                "Credit scores from 620 to 719",
                "Credit score of 720 or greater",
            ],
            purchase_apr_great=0,
        )

        self.assertEqual(
            CardSurveyData.objects.get_summary_statistics(),
            {
                "count": 3,
                "first_report_date": date(2024, 12, 31),
                "report_period_start": date(2024, 7, 1),
                # Poor APRs: 3, 9
                "purchase_apr_poor_count": 2,
                "purchase_apr_poor_min": 3,
                "purchase_apr_poor_max": 9,
                "purchase_apr_poor_pct25": 4.5,
                "purchase_apr_poor_pct75": 7.5,
                # Good APRs: 2, 6
                "purchase_apr_good_count": 2,
                "purchase_apr_good_min": 2,
                "purchase_apr_good_max": 6,
                "purchase_apr_good_pct25": 3,
                "purchase_apr_good_pct75": 5,
                # Great APRs: 0, 1, 3
                "purchase_apr_great_count": 3,
                "purchase_apr_great_min": 0,
                "purchase_apr_great_max": 3,
                "purchase_apr_great_pct25": 0.5,
                "purchase_apr_great_pct75": 2,
            },
        )

    def test_exclude_invalid_aprs(self):
        baker.make(
            CardSurveyData,
            purchase_apr_great=0.5,
            purchase_apr_good=0.25,
        )
        baker.make(
            CardSurveyData,
            purchase_apr_great=0.25,
            purchase_apr_good=0.5,
        )

        qs = CardSurveyData.objects.all()
        self.assertEqual(qs.count(), 2)

        invalid_aprs = qs.only_invalid_aprs()
        self.assertEqual(invalid_aprs.count(), 1)
        self.assertEqual(invalid_aprs[0].purchase_apr_great, 0.5)

        valid_aprs = qs.exclude_invalid_aprs()
        self.assertEqual(valid_aprs.count(), 1)
        self.assertEqual(valid_aprs[0].purchase_apr_great, 0.25)


class CardSurveyDataTests(SimpleTestCase):
    def test_annual_fee_estimated(self):
        tests = [
            [["Annual"], 100, 0, 0, 100],
            [["Monthly"], 0, 10, 0, 120],
            [["Weekly"], 0, 0, 10, 520],
            [["Other"], 0, 0, 0, None],
            [["Annual", "Other"], 100, 0, 0, None],
            [["Annual", "Monthly", "Weekly"], 100, 10, 10, 740],
        ]

        for fee_types, annual, monthly, weekly, expected in tests:
            test = {
                "periodic_fee_type": fee_types,
                "annual_fee": annual,
                "monthly_fee": monthly,
                "weekly_fee": weekly,
            }

            with self.subTest(**test):
                self.assertEqual(
                    CardSurveyData(**test).annual_fee_estimated, expected
                )

    def test_purchase_apr_data_incomplete(self):
        card = CardSurveyData(purchase_apr_offered=True)
        for annotated_column in [
            f"purchase_apr_{tier_column}_{suffix}"
            for (_, tier_column), suffix in product(
                CreditTierColumns, ("min", "max")
            )
        ]:
            setattr(card, annotated_column, None)

        self.assertTrue(card.purchase_apr_data_incomplete)

        card.purchase_apr_good_min = 0.99
        self.assertFalse(card.purchase_apr_data_incomplete)

    def test_issued_by_credit_union(self):
        self.assertTrue(
            CardSurveyData(institution_type="CU").issued_by_credit_union
        )
        self.assertFalse(
            CardSurveyData(institution_type="Bank").issued_by_credit_union
        )

    def test_has_only_variable_late_fees(self):
        self.assertFalse(
            CardSurveyData(
                late_fee_types=[
                    LateFeeTypeChoices[0][0],
                    LateFeeTypeChoices[2][0],
                ]
            ).has_only_variable_late_fees
        )
        self.assertTrue(
            CardSurveyData(
                late_fee_types=[LateFeeTypeChoices[2][0]]
            ).has_only_variable_late_fees
        )

    def test_has_only_variable_over_limit_fees(self):
        self.assertFalse(
            CardSurveyData(
                over_limit_fee_types=[
                    OverlimitFeeTypeChoices[0][0],
                    OverlimitFeeTypeChoices[1][0],
                ]
            ).has_only_variable_over_limit_fees
        )
        self.assertTrue(
            CardSurveyData(
                over_limit_fee_types=[OverlimitFeeTypeChoices[1][0]]
            ).has_only_variable_over_limit_fees
        )
