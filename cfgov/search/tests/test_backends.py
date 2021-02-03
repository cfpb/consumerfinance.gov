import json
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings
from haystack.fields import CharField

from wagtail.core.models import Site

from search.backends.elasticsearch_pages import PageSearchBackend
from search.backends.haystack import CFGOVElasticsearch2SearchBackend
from v1.models import LearnPage


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


class PageSearchBackendTests(TestCase):
    backend_name = 'pages'

    @classmethod
    def setUpTestData(cls):
        cls.root_page = Site.objects.get(is_default_site=True).root_page

        page = LearnPage(
            live=True,
            title='My title',
            slug='my-title',
            content=json.dumps([
                {
                    'type': 'full_width_text',
                    'value': [
                        {
                            'type': 'content',
                            'value': 'My body',
                        },
                    ],
                },
            ])
        )

        page.tags.add('test')

        cls.root_page.add_child(instance=page)

        call_command(
            'wagtail_update_index',
            backend_name=cls.backend_name,
            stdout=StringIO()
        )

    def test_search_no_results(self):
        results = LearnPage.objects.all().search(
            'nothing',
            backend=self.backend_name
        )
        self.assertEqual(results.count(), 0)

    def test_search_title(self):
        results = LearnPage.objects.all().search(
            'My title',
            backend=self.backend_name
        )
        self.assertEqual(results.count(), 1)

    def test_search_body(self):
        results = LearnPage.objects.all().search(
            'My body',
            backend=self.backend_name
        )
        self.assertEqual(results.count(), 1)

    def test_search_filtered_queryset(self):
        results = LearnPage.objects.child_of(self.root_page).search(
            'My body',
            backend=self.backend_name
        )
        self.assertEqual(results.count(), 1)

    def test_search_filtered_by_related_field(self):
        tagged_pages = LearnPage.objects.filter(tags__name='test')
        self.assertEqual(tagged_pages.count(), 1)

        results = tagged_pages.search('My body', backend=self.backend_name)
        self.assertEqual(results.count(), 1)
