from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from search.models import Synonym


class LoadSynonymsTest(TestCase):
    def test_load_synonyms(self):
        out = StringIO()
        call_command("load_synonyms", "search/resources/synonyms_en.txt", stdout=out)
        synonym_count = Synonym.objects.count()
        self.assertGreater(synonym_count, 0)

    def test_load_synonyms_error(self):
        out = StringIO()
        with self.assertRaises(CommandError):
            call_command(
                "load_synonyms", "search/resources/synonyms_ex.txt", stdout=out
            )
