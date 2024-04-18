import os
import shutil
import tempfile
from io import StringIO

from django.core.management import CommandError, call_command
from django.test import TestCase

from tccp.enums import CreditTierColumns
from tccp.models import CardSurveyData

from .baker import baker


class TestValidation(TestCase):
    maxDiff = None

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

    def test_stats(self):
        self.make_test_data()

        self.assertEqual(
            self.call_validate(),
            """
CREDIT SCORE 619 OR LESS
------------------------
Count: 1
Minimum: 10.00%
Maximum: 10.00%
25th percentile: 10.00%
75th percentile: 10.00%

less: 0
average: 0
more: 1

Pay less interest: 1
Transfer a balance: 1
Make a big purchase: 1
Avoid fees: 1
Build credit: 1
Earn rewards: 1

CREDIT SCORES FROM 620 TO 719
-----------------------------
Count: 3
Minimum: 10.00%
Maximum: 30.00%
25th percentile: 15.00%
75th percentile: 25.00%

less: 1
average: 1
more: 1

Pay less interest: 3
Transfer a balance: 3
Make a big purchase: 3
Avoid fees: 3
Build credit: 3
Earn rewards: 3

CREDIT SCORE OF 720 OR GREATER
------------------------------
Count: 3
Minimum: 10.00%
Maximum: 30.00%
25th percentile: 15.00%
75th percentile: 25.00%

less: 1
average: 1
more: 1

Pay less interest: 3
Transfer a balance: 3
Make a big purchase: 3
Avoid fees: 3
Build credit: 3
Earn rewards: 3
""".strip()
            + "\n\n",
        )

    def test_charts(self):
        self.make_test_data()

        self.assertFalse(len(os.listdir(self.tempdir)))
        self.call_validate(save_charts=True)
        self.assertEqual(len(os.listdir(self.tempdir)), 3)
