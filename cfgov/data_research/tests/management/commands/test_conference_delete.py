from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from data_research.models import ConferenceRegistration


class ConferenceDeleteTests(TestCase):
    fixtures = ["conference_registrants.json"]

    def test_deletes_registrants(self):
        self.assertEqual(ConferenceRegistration.objects.count(), 2)
        call_command("conference_delete", "TEST-GOVDELIVERY-CODE", verbosity=0)
        self.assertEqual(ConferenceRegistration.objects.count(), 0)

    def test_writes_to_stdout(self):
        out = StringIO()
        call_command("conference_delete", "TEST-GOVDELIVERY-CODE", stdout=out)
        self.assertEqual(out.getvalue(), "deleting 2 registrants\n")

    def test_deletes_only_provided_govdelivery_code(self):
        self.assertEqual(ConferenceRegistration.objects.count(), 2)
        call_command("conference_delete", "ANOTHER-CODE", verbosity=0)
        self.assertEqual(ConferenceRegistration.objects.count(), 2)
