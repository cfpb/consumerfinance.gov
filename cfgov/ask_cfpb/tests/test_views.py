from __future__ import unicode_literals

import json

from django.apps import apps
from django.core.urlresolvers import NoReverseMatch, reverse
from django.http import Http404, HttpRequest, QueryDict
from django.test import TestCase, override_settings
from django.utils import timezone

from wagtail.wagtailcore.models import Site
from wagtailsharing.models import SharingSite

import mock
from model_mommy import mommy

from ask_cfpb.models import ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG
from ask_cfpb.views import annotate_links, ask_search, redirect_ask_search
from v1.util.migrations import get_or_create_page


now = timezone.now()


class AnswerPagePreviewCase(TestCase):

    def setUp(self):
        from v1.models import HomePage
        from ask_cfpb.models import Answer
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
        self.test_answer = mommy.make(
            Answer,
            answer="Test answer.",
            question="Test question.",
            slug='test-question',
            update_english_page=True,
            update_spanish_page=False)
        self.site = mommy.make(
            Site,
            root_page=self.ROOT_PAGE,
            hostname='localhost',
            port=8000,
            is_default_site=True)
        self.sharing_site = mommy.make(
            SharingSite,
            site=self.site,
            hostname='preview.localhost',
            port=8000)

    @mock.patch('ask_cfpb.views.ServeView.serve_latest_revision')
    def test_preview_page(self, mock_serve):
        from ask_cfpb.views import view_answer
        page = self.test_answer.english_page
        revision = page.save_revision()
        revision.publish()
        test_request = HttpRequest()
        test_request.META['SERVER_NAME'] = 'preview.localhost'
        test_request.META['SERVER_PORT'] = 8000
        view_answer(
            test_request, 'test-question', 'en', self.test_answer.pk)
        self.assertEqual(mock_serve.call_count, 1)

    def test_answer_page_not_live(self):
        from ask_cfpb.views import view_answer
        page = self.test_answer.english_page
        page.live = False
        page.save()
        test_request = HttpRequest()
        with self.assertRaises(Http404):
            view_answer(
                test_request,
                'test-question',
                'en',
                self.test_answer.pk)


class AnswerViewTestCase(TestCase):

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
    def test_en_search_results_page_not_created(self, mock_filter):
        mock_queryset = mock.Mock()
        mock_queryset.count.return_value = 0
        mock_filter.return_value = [mock_queryset]
        response = self.client.get(reverse(
            'ask-search-en'), {'q': 'payday'})
        self.assertEqual(mock_filter.call_count, 1)
        self.assertTrue(mock_filter.called_with(language='en', q='payday'))
        self.assertEqual(response.status_code, 404)

    @mock.patch('ask_cfpb.views.SearchQuerySet')
    def test_en_search(self, mock_sqs):
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

        mock_queryset = mock.Mock()
        mock_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_queryset.count.return_value = 1

        mock_sqs_instance = mock_sqs.return_value.models.return_value
        mock_sqs_instance.filter.return_value = mock_queryset
        mock_sqs_instance.spelling_suggestion.return_value = 'payday'

        response = self.client.get(reverse(
            'ask-search-en'), {'q': 'payday'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['page'],
            mock_page)
        self.assertEqual(
            response.context_data['page'].suggestion,
            None)
        self.assertEqual(mock_sqs_instance.filter.call_count, 1)
        self.assertTrue(mock_sqs_instance.filter.called_with(
            language='en', q='payday'))

    @mock.patch('ask_cfpb.views.SearchQuerySet')
    def test_en_search_no_term(self, mock_sqs):
        from v1.util.migrations import get_or_create_page
        mock_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock results page',
            'ask-cfpb-search-results',
            self.ROOT_PAGE,
            language='en')

        response = self.client.get(reverse(
            'ask-search-en'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['page'],
            mock_page)
        self.assertEqual(
            response.context_data['page'].query,
            '')
        self.assertEqual(
            response.context_data['page'].result_query,
            '')

    @override_settings(FLAGS={'ASK_SEARCH_TYPOS': [('boolean', True)]})
    @mock.patch('ask_cfpb.views.SearchQuerySet')
    def test_en_search_suggestion(self, mock_sqs):
        from v1.util.migrations import get_or_create_page
        mock_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock results page',
            'ask-cfpb-search-results',
            self.english_parent_page,
            language='en',
            live=True)

        mock_return = mock.Mock()
        mock_return.url = 'mockcfpb.gov'
        mock_return.autocomplete = 'A mock question'
        mock_return.text = 'Mock answer text.'

        mock_queryset = mock.Mock()
        mock_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_queryset.count.return_value = 0

        mock_sqs_instance = mock_sqs.return_value.models.return_value
        mock_sqs_instance.filter.return_value = mock_queryset
        mock_sqs_instance.spelling_suggestion.return_value = 'payday'

        response = self.client.get(reverse(
            'ask-search-en'), {'q': 'paydya'})
        self.assertEqual(response.status_code, 200)
        response_page = response.context_data['page']

        self.assertEqual(response_page, mock_page)
        self.assertEqual(response_page.suggestion, 'paydya')
        self.assertEqual(response_page.result_query, 'payday')
        self.assertEqual(response_page.query, 'paydya')

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
    def test_es_search(self, mock_filter):
        get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock Spanish results page',
            'respuestas',
            self.spanish_parent_page,
            language='es',
            live=True)
        mock_return = mock.Mock()
        mock_return.url = 'mockcfpb.gov'
        mock_return.autocomplete = 'A mock question'
        mock_return.text = 'Mock answer text.'
        mock_queryset = mock.Mock()
        mock_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_queryset.count.return_value = 1
        mock_filter.return_value = mock_queryset
        self.client.get(reverse(
            'ask-search-es', kwargs={'language': 'es'}), {'q': 'payday'})
        self.assertEqual(mock_filter.call_count, 1)
        self.assertTrue(mock_filter.called_with(language='es', q='payday'))

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_search_page_en_selection(self, mock_filter):
        page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock results page',
            'ask-cfpb-search-results',
            self.english_parent_page,
            language='en',
            live=True)
        mock_return = mock.Mock()
        mock_return.url = 'url'
        mock_return.autocomplete = 'question text'
        mock_queryset = mock.Mock()
        mock_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_queryset.count.return_value = 1
        mock_filter.return_value = mock_queryset
        self.client.get(reverse(
            'ask-search-en'), {'q': 'tuition'})
        self.assertEqual(mock_filter.call_count, 1)
        self.assertEqual(page.language, 'en')
        self.assertEqual(page.answers, [])
        self.assertEqual(
            page.get_template(HttpRequest()),
            'ask-cfpb/answer-search-results.html')

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_search_page_es_selection(self, mock_filter):
        page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock Spanish results page',
            'respuestas',
            self.spanish_parent_page,
            language='es',
            live=True)
        mock_return = mock.Mock()
        mock_return.url = 'url'
        mock_return.autocomplete = 'question text'
        mock_queryset = mock.Mock()
        mock_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_queryset.count.return_value = 1
        mock_filter.return_value = mock_queryset
        self.client.get(reverse(
            'ask-search-es', kwargs={'language': 'es'}), {'q': 'hipotecas'})
        self.assertEqual(mock_filter.call_count, 1)
        self.assertEqual(page.language, 'es')
        self.assertEqual(page.answers, [])
        self.assertEqual(
            page.get_template(HttpRequest()),
            'ask-cfpb/answer-search-spanish-results.html')

    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_json_response(self, mock_filter):
        get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock results page',
            'ask-cfpb-search-results',
            self.english_parent_page,
            language='en',
            live=True)
        mock_return = mock.Mock()
        mock_return.url = "inscisive_url.com"
        mock_return.autocomplete = "inscisive question"
        mock_return.text = "inscisive text"
        mock_queryset = mock.Mock()
        mock_queryset.__iter__ = mock.Mock(return_value=iter([mock_return]))
        mock_queryset.count.return_value = 1
        mock_filter.return_value = mock_queryset
        response = self.client.get(reverse(
            'ask-search-en-json',
            kwargs={'as_json': 'json'}), {'q': 'tuition'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_filter.call_count, 1)
        self.assertEqual(json.loads(response.content)['query'], 'tuition')

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


class RedirectAskSearchTestCase(TestCase):

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
                         '/ask-cfpb/category-my_category/')

    def test_redirect_search_with_audience(self):
        audience_querystring = (
            'selected_facets=audience_exact:Older+Americans'
            '&selected_facets=audience_exact:my_audience2')
        request = HttpRequest()
        request.GET = QueryDict(audience_querystring)
        result = redirect_ask_search(request)
        self.assertEqual(
            result.get('location'),
            '/ask-cfpb/audience-older-americans/')

    def test_spanish_redirect_search_with_tag(self):
        target_tag = 'spanishtag1'
        tag_querystring = (
            'selected_facets=tag_exact:{}'
            '&selected_facets=tag_exact:spanishtag2'.format(target_tag))
        request = HttpRequest()
        request.GET = QueryDict(tag_querystring)
        result = redirect_ask_search(request, language='es')
        self.assertEqual(
            result.get('location'),
            '/es/obtener-respuestas/buscar-por-etiqueta/{}/'.format(
                target_tag))

    def test_english_redirect_search_with_tag(self):
        target_tag = 'englishtag1'
        tag_querystring = (
            'selected_facets=tag_exact:{}'
            '&selected_facets=tag_exact:englishtag2'.format(target_tag))
        request = HttpRequest()
        request.GET = QueryDict(tag_querystring)
        result = redirect_ask_search(request, language='en')
        self.assertEqual(
            result.get('location'),
            '/ask-cfpb/search-by-tag/{}/'.format(
                target_tag))

    def test_redirect_search_with_unrecognized_facet_raises_404(self):
        querystring = \
            'sort=-updated_at&selected_facets=imtkfidycqszgfdb&page=60'
        request = HttpRequest()
        request.GET = QueryDict(querystring)
        with self.assertRaises(Http404):
            redirect_ask_search(request)
