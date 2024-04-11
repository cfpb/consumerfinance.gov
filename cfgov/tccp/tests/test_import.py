import os.path
from io import StringIO

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase

from tccp.models import CardSurveyData


class TestImport(TestCase):
    def call_import(self, filename):
        test_filename = os.path.join(
            os.path.dirname(__file__), "data", filename
        )
        out = StringIO()
        call_command("import_tccp", test_filename, stdout=out, stderr=out)

    def test_import(self):
        self.call_import("sample.xlsx")
        self.assertEqual(CardSurveyData.objects.count(), 5)
        self.assertEqual(
            CardSurveyData.objects.filter(
                targeted_credit_tiers__contains="Credit score 619 or less"
            ).count(),
            2,
        )

    def test_invalid_import(self):
        with self.assertRaises(ValidationError):
            self.call_import("sample-invalid.xlsx")
