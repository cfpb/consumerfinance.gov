# -*- coding: utf-8 -*-
import tempfile

from django.core.management import call_command
from django.test import TestCase

from openpyxl import load_workbook


class ConferenceExportTests(TestCase):
    fixtures = ["conference_registrants.json"]

    def test_export_writes_valid_excel_workbook(self):
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as f:
            call_command("conference_export", "TEST-GOVDELIVERY-CODE", f.name)

            workbook = load_workbook(f.name)
            self.assertEqual(workbook.active["C2"].value, "My Name")
            self.assertEqual(workbook.active["C3"].value, "Name with Unicodë")
