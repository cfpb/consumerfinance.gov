from __future__ import unicode_literals

import json
import mock

from model_mommy import mommy

from ask_cfpb.models.pages import AnswerResultsPage
from django.apps import apps
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import HttpRequest
import django.test
from django.test import Client
from django.utils import timezone
from v1.util.migrations import get_or_create_page, get_free_path

client = Client()
now = timezone.now()


class AnswerViewTestCase(django.test.TestCase):

    def setUp(self):
        from v1.models import HomePage
        from ask_cfpb.models import ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG
        ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.english_parent_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerLandingPage',
            'Ask CFPB',
            ENGLISH_PARENT_SLUG,
            ROOT_PAGE,
            language='en',
            live=True)
        self.spanish_parent_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerLandingPage',
            'Obtener respuestas',
            SPANISH_PARENT_SLUG,
            ROOT_PAGE,
            language='es',
            live=True)

    def create_answer_results_page(self, **kwargs):
        kwargs.setdefault(
            'path', get_free_path(apps, self.english_parent_page))
        kwargs.setdefault('depth', self.english_parent_page.depth + 1)
        kwargs.setdefault('slug', 'mock-answer-page-en-1234')
        kwargs.setdefault('title', 'Mock answer page title')
        page = mommy.prepare(AnswerResultsPage, **kwargs)
        page.save()
        return page

    def test_bad_language_search(self):
        with self.assertRaises(NoReverseMatch):
            client.get(reverse(
                'ask-search-en',
                kwargs={'language': 'zz'}), {'q': 'payday'})

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_en_search(self, mock_query):
        client.get(reverse(
            'ask-search-en'), {'q': 'payday'})
        self.assertEqual(mock_query.call_count, 1)
        self.assertTrue(mock_query.called_with(language='en', q='payday'))

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_es_search(self, mock_query):
        client.get(reverse(
            'ask-search-es', kwargs={'language': 'es'}), {'q': 'payday'})
        self.assertEqual(mock_query.call_count, 1)
        self.assertTrue(mock_query.called_with(language='es', q='payday'))

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_search_page_en_selection(self, mock_query):
        return_mock = mock.Mock()
        mock_query.return_value = [return_mock]
        return_mock.url = 'url'
        return_mock.autocomplete = 'question text'
        page = self.create_answer_results_page(language='en')
        client.get(reverse(
            'ask-search-en'))
        self.assertEqual(mock_query.call_count, 1)
        self.assertEqual(page.language, 'en')
        self.assertEqual(page.answers, [])
        self.assertEqual(
            page.get_template(HttpRequest()),
            'ask-cfpb/answer-search-results.html')

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_search_page_es_selection(self, mock_query):
        return_mock = mock.Mock()
        mock_query.return_value = [return_mock]
        return_mock.url = 'url'
        return_mock.autocomplete = 'question text'
        page = self.create_answer_results_page(language='es')
        client.get(reverse(
            'ask-search-es',
            kwargs={'language': 'es'}))
        self.assertEqual(mock_query.call_count, 1)
        self.assertEqual(page.language, 'es')
        self.assertEqual(page.answers, [])
        self.assertEqual(
            page.get_template(HttpRequest()),
            'ask-cfpb/answer-search-spanish-results.html')

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_en_search_as_json(self, mock_query):
        mock_query.autocomplete.return_value = ['question text']
        mock_query.url.return_value = ['answer/url']
        client.get(reverse(
            'ask-search-en-json',
            kwargs={'as_json': 'json'}))
        self.assertEqual(mock_query.call_count, 1)
        self.assertTrue(
            mock_query.called_with(
                language='en',
                as_json='json'))

    @mock.patch('ask_cfpb.views.SearchQuerySet.autocomplete')
    def test_autocomplete_en(self, mock_autocomplete):
        mock_autocomplete.return_value = json.dumps({'url': 'url',
                                                     'question': 'question'})
        result = client.get(reverse(
            'ask-autocomplete-en'), {'q': 'payday'})
        self.assertEqual(mock_autocomplete.call_count, 1)
        self.assertTrue(
            mock_autocomplete.called_with(language='en', q='payday'))
        output = json.loads(result.content)
        self.assertEqual(
            sorted(json.loads(output).keys()),
            ['question', 'url'])

    @mock.patch('ask_cfpb.views.SearchQuerySet.autocomplete')
    def test_autocomplete_es(self, mock_autocomplete):
        mock_autocomplete.return_value = json.dumps({'url': 'url',
                                                     'question': 'question'})
        result = client.get(reverse(
            'ask-autocomplete-es',
            kwargs={'language': 'es'}), {'q': 'payday'})
        self.assertEqual(mock_autocomplete.call_count, 1)
        self.assertTrue(
            mock_autocomplete.called_with(language='es', q='payday'))
        output = json.loads(result.content)
        self.assertEqual(
            sorted(json.loads(output).keys()),
            ['question', 'url'])
