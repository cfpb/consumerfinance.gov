import os
import shutil
import tempfile
from io import StringIO

from django.core.management import CommandError, call_command
from django.test import SimpleTestCase, TestCase

from tccp.enums import CreditTierColumns
from tccp.management.commands.validate_tccp import fmt_range
from tccp.models import CardSurveyData

from .baker import baker


class TestValidationFormatting(SimpleTestCase):
    def test_fmt_single_value(self):
        self.assertEqual(fmt_range(0.1235, 0.1235), "12.35%")

    def test_fmt_range(self):
        self.assertEqual(fmt_range(0.1235, 0.5), "12.35% - 50%")


class TestValidation(TestCase):
    def setUp(self):
        self.dir = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

    def tearDown(self):
        os.chdir(self.dir)
        shutil.rmtree(self.tempdir)

    def call_validate(self, **kwargs):
        out = StringIO()
        call_command("validate_tccp", stdout=out, stderr=out, **kwargs)
        return out.getvalue()

    def test_error_if_no_data_loaded(self):
        with self.assertRaises(CommandError) as e:
            self.call_validate()

        self.assertEqual(str(e.exception), "No cards in dataset!")

    def test_error_if_insufficient_data_for_all_situations(self):
        baker.make(CardSurveyData)
        with self.assertRaises(CommandError) as e:
            self.call_validate()

        self.assertEqual(str(e.exception), "Situation with no results!")

    def make_test_data(self):
        for i, (name, column) in enumerate(CreditTierColumns):
            for j in range(3 if i else 1):
                baker.make(
                    CardSurveyData,
                    availability_of_credit_card_plan="National",
                    targeted_credit_tiers=[name],
                    rewards=["Cashback rewards"],
                    **{
                        f"purchase_apr_{column}": (j + 1) * 0.1,
                        f"transfer_apr_{column}": 0.99,
                    },
                )

        # Also create an invalid card to be filtered out.
        baker.make(
            CardSurveyData,
            slug="invalid-card",
            purchase_apr_great=0.5,
            purchase_apr_poor=0.25,
        )

    def test_stats(self):
        self.make_test_data()

        self.assertEqual(
            self.call_validate(),
            """
8 cards in database
1 cards with invalid APRs
1: invalid-card

CREDIT SCORE 619 OR LESS
------------------------
Count: 1
Minimum: 10%
Maximum: 10%
25th percentile: 10%
75th percentile: 10%

less: None
average: None
more: 10%

Pay less interest: 1
Transfer a balance: 1
Make a big purchase: 1
Avoid fees: 1
Build credit: 1
Earn rewards: 1

CREDIT SCORES FROM 620 TO 719
-----------------------------
Count: 3
Minimum: 10%
Maximum: 30%
25th percentile: 15%
75th percentile: 25%

less: 10%
average: 20%
more: 30%

Pay less interest: 3
Transfer a balance: 3
Make a big purchase: 3
Avoid fees: 3
Build credit: 3
Earn rewards: 3

CREDIT SCORE OF 720 OR GREATER
------------------------------
Count: 3
Minimum: 10%
Maximum: 30%
25th percentile: 15%
75th percentile: 25%

less: 10%
average: 20%
more: 30%

Pay less interest: 3
Transfer a balance: 3
Make a big purchase: 3
Avoid fees: 3
Build credit: 3
Earn rewards: 3
""".strip()
            + "\n\n",
        )
