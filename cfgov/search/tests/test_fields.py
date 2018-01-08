from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.utils import override_settings

from search.fields import CharFieldWithSynonyms


class CharFieldWithSynonymsTestCase(TestCase):

    @override_settings(ELASTICSEARCH_INDEX_SETTINGS={
        'settings': {'analysis': {'analyzer': {'synonym_en': {}}}}
    })
    def test_synonym_analyzer(self):
        text_field = CharFieldWithSynonyms(document=True, use_template=True,
                                           index_fieldname='synonymous_text')
        self.assertEqual(text_field.analyzer, 'synonym_en')

    @override_settings(ELASTICSEARCH_INDEX_SETTINGS={
        'settings': {'analysis': {'analyzer': {}}}
    })
    def test_synonym_analyzer_does_not_exist(self):
        with self.assertRaises(ImproperlyConfigured):
            CharFieldWithSynonyms(document=True, use_template=True,
                                  index_fieldname='synonymous_text')
