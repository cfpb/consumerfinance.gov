from django.test import TestCase

from search.fields import CharFieldWithSynonyms


class CharFieldWithSynonymsTestCase(TestCase):
    def test_synonym_analyzer(self):
        text_field = CharFieldWithSynonyms(document=True, use_template=True,
                                           index_fieldname='synonymous_text')
        self.assertEqual(text_field.analyzer, 'synonym')
