from __future__ import unicode_literals

import json
import mock

from django.apps import apps
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import HttpRequest
import django.test
from django.test import Client
from django.utils import timezone

from ask_cfpb.models.pages import AnswerResultsPage

client = Client()
now = timezone.now()


class AnswerViewTestCase(django.test.TestCase):

    def setUp(self):
        from v1.models import HomePage
        self.ROOT_PAGE = HomePage.objects.get(slug='cfgov')

    def test_bad_language_search(self):
        with self.assertRaises(NoReverseMatch):
            client.get(reverse(
                'ask-search-en',
                kwargs={'language': 'zz'}), {'q': 'payday'})

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_en_search_no_such_page(self, mock_query):
        response = client.get(reverse(
            'ask-search-en'), {'q': 'payday'})
        self.assertEqual(mock_query.call_count, 1)
        self.assertTrue(mock_query.called_with(language='en', q='payday'))
        self.assertEqual(response.status_code, 404)

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_en_search(self, mock_query):
        from v1.util.migrations import get_or_create_page
        mock_page = get_or_create_page(  # noqa
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock results page',
            'ask-cfpb-search-results',
            self.ROOT_PAGE,
            language='en')
        mock_return = mock.Mock()
        mock_return.url = 'mockcfpb.gov'
        mock_return.autocomplete = 'A mock question'
        mock_return.text = 'Mock answer text.'
        mock_query.return_value = [mock_return]
        response = client.get(reverse(
            'ask-search-en'), {'q': 'payday'})
        # import pdb; pdb.set_trace()
        self.assertEqual(mock_query.call_count, 1)
        self.assertTrue(mock_query.called_with(language='en', q='payday'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['page'],
            mock_page)

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
        page = AnswerResultsPage(
            language='en',
            depth=3,
            slug='results',
            path=001001001,
            title='Results')
        page.save()
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
        page = AnswerResultsPage(
            language='es',
            depth=3,
            slug='results',
            path=001001001,
            title='Results')
        page.save()
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
