from __future__ import unicode_literals

import json
import mock

from model_mommy import mommy

from django.apps import apps
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import HttpRequest, Http404, QueryDict
import django.test
from django.utils import timezone
from wagtail.wagtailcore.models import Site

from ask_cfpb.models import (
    AnswerResultsPage, ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG)
from ask_cfpb.views import annotate_links, redirect_ask_search, ask_search
from v1.util.migrations import get_or_create_page, get_free_path

now = timezone.now()


class AnswerViewTestCase(django.test.TestCase):

    def setUp(self):
        from v1.models import HomePage
        self.ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.english_parent_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerLandingPage',
            'Ask CFPB',
            ENGLISH_PARENT_SLUG,
            self.ROOT_PAGE,
            language='en',
            live=True)
        self.spanish_parent_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerLandingPage',
            'Obtener respuestas',
            SPANISH_PARENT_SLUG,
            self.ROOT_PAGE,
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

    def test_annotate_links(self):
        mock_answer = (
            '<p>Answer with a <a href="http://fake.com">fake link.</a></p>')
        (annotated_answer, links) = annotate_links(mock_answer)
        self.assertEqual(
            annotated_answer,
            '<html><body><p>Answer with a <a href="http://fake.com">fake '
            'link.</a><sup>1</sup></p></body></html>')
        self.assertEqual(links, [(1, str('http://fake.com'))])

    def test_annotate_links_no_href(self):
        mock_answer = (
            '<p>Answer with a <a>fake link.</a></p>')
        (annotated_answer, links) = annotate_links(mock_answer)
        self.assertEqual(links, [])

    def test_annotate_links_no_site(self):
        site = Site.objects.get(is_default_site=True)
        site.is_default_site = False
        site.save()
        with self.assertRaises(RuntimeError) as context:
            annotate_links('answer')
        self.assertIn('no default wagtail site', str(context.exception))

    def test_bad_language_search(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse(
                'ask-search-en',
                kwargs={'language': 'zz'}), {'q': 'payday'})

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_en_search_no_such_page(self, mock_query):
        response = self.client.get(reverse(
            'ask-search-en'), {'q': 'payday'})
        self.assertEqual(mock_query.call_count, 1)
        self.assertTrue(mock_query.called_with(language='en', q='payday'))
        self.assertEqual(response.status_code, 404)

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_en_search(self, mock_query):
        from v1.util.migrations import get_or_create_page
        mock_page = get_or_create_page(
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
        response = self.client.get(reverse(
            'ask-search-en'), {'q': 'payday'})
        self.assertEqual(mock_query.call_count, 1)
        self.assertTrue(mock_query.called_with(language='en', q='payday'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['page'],
            mock_page)

    @mock.patch('ask_cfpb.views.redirect_ask_search')
    def test_ask_search_encounters_facets(self, mock_redirect):
        request = HttpRequest()
        request.GET['selected_facets'] = 'category_exact:my_category'
        ask_search(request)
        self.assertEqual(mock_redirect.call_count, 1)

    @mock.patch('ask_cfpb.views.redirect')
    def test_redirect_ask_search_passes_query_string(self, mock_redirect):
        request = HttpRequest()
        request.GET['q'] = 'hoodoo'
        redirect_ask_search(request)
        self.assertEqual(mock_redirect.call_count, 1)

    @mock.patch('ask_cfpb.views.redirect')
    def test_spanish_redirect_ask_search_passes_query_string(
            self, mock_redirect):
        request = HttpRequest()
        request.GET['selected_facets'] = 'category_exact:my_categoria'
        redirect_ask_search(request, language='es')
        self.assertEqual(mock_redirect.call_count, 1)

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_es_search(self, mock_query):
        self.client.get(reverse(
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
        self.client.get(reverse(
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
        self.client.get(reverse(
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
        self.client.get(reverse(
            'ask-search-en-json',
            kwargs={'as_json': 'json'}))
        self.assertEqual(mock_query.call_count, 1)
        self.assertTrue(
            mock_query.called_with(
                language='en',
                as_json='json'))

    def test_autocomplete_en_blank_term(self):
        result = self.client.get(reverse(
            'ask-autocomplete-en'), {'term': ''})
        output = json.loads(result.content)
        self.assertEqual(output, [])

    def test_autocomplete_es_blank_term(self):
        result = self.client.get(reverse(
            'ask-autocomplete-es',
            kwargs={'language': 'es'}), {'term': ''})
        output = json.loads(result.content)
        self.assertEqual(output, [])

    @mock.patch('ask_cfpb.views.SearchQuerySet.autocomplete')
    def test_autocomplete_en(self, mock_autocomplete):
        mock_search_result = mock.Mock()
        mock_search_result.autocomplete = 'question'
        mock_search_result.url = 'url'
        mock_autocomplete.return_value = [mock_search_result]
        result = self.client.get(reverse(
            'ask-autocomplete-en'), {'term': 'question'})
        self.assertEqual(mock_autocomplete.call_count, 1)
        output = json.loads(result.content)
        self.assertEqual(
            sorted(output[0].keys()),
            ['question', 'url'])

    @mock.patch('ask_cfpb.views.SearchQuerySet.autocomplete')
    def test_autocomplete_es(self, mock_autocomplete):
        mock_search_result = mock.Mock()
        mock_search_result.autocomplete = 'question'
        mock_search_result.url = 'url'
        mock_autocomplete.return_value = [mock_search_result]
        result = self.client.get(reverse(
            'ask-autocomplete-es',
            kwargs={'language': 'es'}), {'term': 'question'})
        self.assertEqual(mock_autocomplete.call_count, 1)
        output = json.loads(result.content)
        self.assertEqual(
            sorted(output[0].keys()),
            ['question', 'url'])


class RedirectAskSearchTestCase(django.test.TestCase):

    def test_redirect_search_no_facets(self):
        request = HttpRequest()
        with self.assertRaises(Http404):
            redirect_ask_search(request)

    def test_redirect_search_blank_facets(self):
        request = HttpRequest()
        request.GET['selected_facets'] = ''
        with self.assertRaises(Http404):
            redirect_ask_search(request)

    def test_redirect_search_no_query(self):
        request = HttpRequest()
        request.GET['q'] = ' '
        with self.assertRaises(Http404):
            redirect_ask_search(request)

    def test_redirect_search_with_category(self):
        category_querystring = (
            'selected_facets=category_exact:my_category'
            '&selected_facets=category_exact:my_category2'
            '&selected_facets=audience_exact:Older+Americans'
            '&selected_facets=audience_exact:my_audience2'
            '&selected_facets=tag_exact:mytag1'
            '&selected_facets=tag_exact:mytag2')
        request = HttpRequest()
        request.GET = QueryDict(category_querystring)
        result = redirect_ask_search(request)
        self.assertEqual(result.get('location'),
                         '/ask-cfpb/category-my_category')

    def test_redirect_search_with_audience(self):
        audience_querystring = (
            'selected_facets=audience_exact:Older+Americans'
            '&selected_facets=audience_exact:my_audience2')
        request = HttpRequest()
        request.GET = QueryDict(audience_querystring)
        result = redirect_ask_search(request)
        self.assertEqual(
            result.get('location'),
            '/ask-cfpb/audience-older-americans')

    def test_redirect_search_with_tag(self):
        target_tag = 'mytag1'
        tag_querystring = (
            'selected_facets=tag_exact:{}'
            '&selected_facets=tag_exact:mytag2'.format(target_tag))
        request = HttpRequest()
        request.GET = QueryDict(tag_querystring)
        result = redirect_ask_search(request, language='es')
        self.assertEqual(
            result.get('location'),
            '/es/obtener-respuestas/buscar-por-etiqueta/{}/'.format(
                target_tag))

    def test_redirect_search_with_english_tag_raises_404(self):
        """Only Spanish tags are supported"""
        target_tag = 'mytag1'
        tag_querystring = (
            'selected_facets=tag_exact:{}'
            '&selected_facets=tag_exact:mytag2'.format(target_tag))
        request = HttpRequest()
        request.GET = QueryDict(tag_querystring)
        with self.assertRaises(Http404):
            redirect_ask_search(request, language='en')
