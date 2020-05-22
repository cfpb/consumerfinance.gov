from django.test import TestCase
from django.test.utils import override_settings
from haystack.fields import CharField

from search.backends import CFGOVElasticsearch2SearchBackend


class CFGOVElasticsearch2SearchBackendTestCase(TestCase):

    @override_settings(ELASTICSEARCH_INDEX_SETTINGS={
        'settings': {'some': 'settings'}
    })
    def test_user_settings(self):
        backend = CFGOVElasticsearch2SearchBackend(
            'default', URL='http://localhost:9200', INDEX_NAME='test_index')
        self.assertEqual(
            backend.DEFAULT_SETTINGS,
            {'settings': {'some': 'settings'}}
        )

    @override_settings(ELASTICSEARCH_DEFAULT_ANALYZER='lacan')
    def test_overrides_default_analyzer(self):
        backend = CFGOVElasticsearch2SearchBackend(
            'default', URL='http://localhost:9200', INDEX_NAME='test_index')
        self.assertEqual(backend.DEFAULT_ANALYZER, 'lacan')

    def test_build_schema_default(self):
        backend = CFGOVElasticsearch2SearchBackend(
            'default', URL='http://localhost:9200', INDEX_NAME='test_index')
        text_field = CharField(document=True, use_template=True,
                               index_fieldname='text')
        schema = backend.build_schema({'text': text_field})
        self.assertEqual('snowball', schema[1]['text']['analyzer'])

    def test_build_schema_custom(self):
        backend = CFGOVElasticsearch2SearchBackend(
            'default', URL='http://localhost:9200', INDEX_NAME='test_index')
        text_field = CharField(document=True, use_template=True,
                               index_fieldname='text')
        text_field.analyzer = 'lacan'
        schema = backend.build_schema({'text': text_field})
        self.assertEqual('lacan', schema[1]['text']['analyzer'])
