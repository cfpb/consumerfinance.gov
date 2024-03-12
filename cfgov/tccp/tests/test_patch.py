import tempfile
from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from tccp.models import CardSurveyData

from .baker import baker


class TestImport(TestCase):
    def setUp(self):
        for institution in ["Foo", "Bar", "Baz"]:
            baker.make(
                CardSurveyData,
                institution_name=institution,
                top_25_institution=False,
            )

    def call_patch(self, file_contents):
        with tempfile.NamedTemporaryFile("w") as f:
            f.write(file_contents)
            f.flush()

            out = StringIO()
            call_command("patch_tccp", f.name, stdout=out, stderr=out)

    def test_patch_success(self):
        self.assertEqual(
            CardSurveyData.objects.filter(top_25_institution=True).count(),
            0,
        )
        self.call_patch("Foo\nBaz")
        self.assertEqual(
            CardSurveyData.objects.filter(top_25_institution=True).count(),
            2,
        )

    def test_failure(self):
        with self.assertRaises(CommandError):
            self.call_patch("Invalid")
