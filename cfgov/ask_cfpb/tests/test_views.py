from __future__ import unicode_literals

import json
import unittest

from django.apps import apps
from django.core.urlresolvers import NoReverseMatch, reverse
from django.http import Http404, HttpRequest, QueryDict
from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone

from wagtail.wagtailcore.models import Site
from wagtailsharing.models import SharingSite

import mock
from model_mommy import mommy

from ask_cfpb.models import (
    ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG, Answer, AnswerPage
)
from ask_cfpb.models.search import make_safe
from ask_cfpb.tests.models.test_pages import mock_queryset
from ask_cfpb.views import (
    annotate_links, ask_search, redirect_ask_search, view_answer
)
from v1.util.migrations import get_or_create_page


now = timezone.now()


class AskSearchSafetyCase(unittest.TestCase):

    def test_make_safe(self):
        test_phrase = 'Would you like green eggs and ^~`[]#<>;|%\\{\\}\\?'
        self.assertEqual(
            make_safe(test_phrase),
            'Would you like green eggs and ?'
        )


class AnswerPagePreviewCase(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)
        self.english_parent_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerLandingPage',
            'Ask CFPB',
            ENGLISH_PARENT_SLUG,
            self.default_site.root_page,
            language='en',
            live=True)

    def make_request(self, slug, **kwargs):
        path = '/{}/{}/'.format(ENGLISH_PARENT_SLUG, slug)
        request = RequestFactory().get(path, **kwargs)
        request.site = self.default_site
        return request

    def test_view_answer_for_nonexistent_page_raises_404(self):
        with self.assertRaises(Http404):
            view_answer(
                self.make_request('this-doesnt-exist-en-9999'),
                slug='this-doesnt-exist',
                language='en',
                answer_id=9999
            )

    def test_view_answer_for_unpublished_page_raises_404(self):
        answer = mommy.make(Answer)
        answer_page = AnswerPage(
            title='question1',
            answer_base=answer,
            slug='question1-en-{}'.format(answer.pk),
            question='Question 1',
            live=False
        )
        self.english_parent_page.add_child(instance=answer_page)

        with self.assertRaises(Http404):
            view_answer(
                self.make_request(answer_page.slug),
                slug='question1',
                language='en',
                answer_id=answer.pk
            )

    def test_view_answer_for_live_page_returns_correct_content(self):
        answer = mommy.make(Answer)
        answer_page = AnswerPage(
            title='question1',
            answer_base=answer,
            slug='question1-en-{}'.format(answer.pk),
            question='Question 1',
            live=True
        )
        self.english_parent_page.add_child(instance=answer_page)

        response = view_answer(
            self.make_request(answer_page.slug),
            'question1',
            'en',
            answer.pk
        )
        self.assertContains(response, 'Question 1')

    def test_view_answer_using_wagtail_sharing_returns_draft_content(self):
        answer = mommy.make(Answer)
        answer_page = AnswerPage(
            title='question1',
            answer_base=answer,
            slug='question1-en-{}'.format(answer.pk),
            question='Question 1',
            live=True
        )
        self.english_parent_page.add_child(instance=answer_page)

        answer_page.question = 'Draft!!!'
        answer_page.save_revision()

        live_request = self.make_request(answer_page.slug)

        live_response = view_answer(
            live_request,
            'question1',
            'en',
            answer.pk
        )
        self.assertNotContains(live_response, 'Draft!!!')

        sharing_site = SharingSite.objects.get(site=self.default_site)
        draft_request = self.make_request(
            answer_page.slug,
            SERVER_NAME=sharing_site.hostname,
            SERVER_PORT=sharing_site.port
        )

        draft_response = view_answer(
            draft_request,
            'question1',
            'en',
            answer.pk
        )
        self.assertContains(draft_response, 'Draft!!!')

    def test_view_answer_page_redirected_to_other_page(self):
        answer2 = mommy.make(Answer)
        answer_page2 = AnswerPage(
            title='Question 2',
            answer_base=answer2,
            slug='question2-en-{}'.format(answer2.pk),
            live=True
        )
        self.english_parent_page.add_child(instance=answer_page2)

        answer1 = mommy.make(Answer)
        answer_page1 = AnswerPage(
            title='Question 1',
            answer_base=answer1,
            redirect_to_page=answer_page2,
            slug='question1-en-{}'.format(answer1.pk),
            live=True
        )
        self.english_parent_page.add_child(instance=answer_page1)

        response = self.client.get(answer_page1.url)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, answer_page2.url)


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

    def test_en_search_results_page_not_created(self):
        response = self.client.get(reverse(
            'ask-search-en'), {'q': 'payday'})
        self.assertEqual(response.status_code, 404)

    @mock.patch('ask_cfpb.views.AskSearch')
    def test_en_search(self, mock_ask_search):
        from v1.util.migrations import get_or_create_page
        mock_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock results page',
            'ask-cfpb-search-results',
            self.ROOT_PAGE,
            language='en')

        mock_ask_search.queryset = mock_queryset(count=3)
        mock_ask_search.suggestion = None
        mock_ask_search.search_term = 'payday'
        response = self.client.get(reverse(
            'ask-search-en'), {'q': 'payday'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['page'], mock_page)
        self.assertEqual(mock_ask_search.call_count, 1)
        self.assertTrue(mock_ask_search.called_with(
            language='en', search_term='payday'))

    @mock.patch('ask_cfpb.views.AskSearch')
    def test_en_search_no_term(self, mock_ask_search):
        from v1.util.migrations import get_or_create_page
        mock_page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock results page',
            'ask-cfpb-search-results',
            self.ROOT_PAGE,
            language='en')
        mock_ask_search.queryset = mock_queryset()
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
    @mock.patch('ask_cfpb.models.search.SearchQuerySet.spelling_suggestion')
    @mock.patch('ask_cfpb.models.search.SearchQuerySet.filter')
    def test_en_search_suggestion(self, mock_filter, mock_suggestion):
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

        # AskSearch.sugggest flips search_term and suggestion when called
        mock_filter.return_value = mock_queryset(count=0)
        mock_suggestion.return_value = 'payday'
        response = self.client.get(reverse(
            'ask-search-en'), {'q': 'paydya'})
        self.assertEqual(response.status_code, 200)
        response_page = response.context_data['page']
        self.assertEqual(response_page, mock_page)
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

    @mock.patch('ask_cfpb.views.AskSearch')
    def test_es_search(self, mock_ask_search):
        get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock Spanish results page',
            'respuestas',
            self.spanish_parent_page,
            language='es',
            live=True)
        mock_ask_search.queryset = mock_queryset(count=1)
        mock_ask_search.suggestion = None
        mock_ask_search.search_term = 'payday'
        self.client.get(reverse(
            'ask-search-es', kwargs={'language': 'es'}), {'q': 'payday'})
        self.assertEqual(mock_ask_search.call_count, 1)
        self.assertTrue(mock_ask_search.called_with(
            language='es', search_term='payday'))

    @mock.patch('ask_cfpb.views.AskSearch')
    def test_search_page_en_selection(self, mock_search):
        page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock results page',
            'ask-cfpb-search-results',
            self.english_parent_page,
            language='en',
            live=True)
        mock_search.serch_term = 'tuition'
        mock_search.queryset = mock_queryset(count=1)
        response = self.client.get(reverse(
            'ask-search-en'), {'q': 'tuition'})
        self.assertEqual(mock_search.call_count, 1)
        self.assertEqual(response.context_data.get('page').language, 'en')
        self.assertEqual(
            page.get_template(HttpRequest()),
            'ask-cfpb/answer-search-results.html')

    @mock.patch('ask_cfpb.views.AskSearch')
    def test_search_page_es_selection(self, mock_search):
        page = get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock Spanish results page',
            'respuestas',
            self.spanish_parent_page,
            language='es',
            live=True)
        mock_search.serch_term = 'hipotecas'
        mock_search.queryset = mock_queryset(count=5)
        response = self.client.get(reverse(
            'ask-search-es', kwargs={'language': 'es'}), {'q': 'hipotecas'})
        self.assertEqual(page.answers, [])
        self.assertEqual(mock_search.call_count, 1)
        self.assertEqual(response.context_data['page'].language, 'es')
        self.assertEqual(
            page.get_template(HttpRequest()),
            'ask-cfpb/answer-search-results.html')

    @mock.patch('ask_cfpb.views.SearchQuerySet.spelling_suggestion')
    @mock.patch('ask_cfpb.views.SearchQuerySet.filter')
    def test_json_response(self, mock_filter, mock_suggestion):
        get_or_create_page(
            apps,
            'ask_cfpb',
            'AnswerResultsPage',
            'Mock results page',
            'ask-cfpb-search-results',
            self.english_parent_page,
            language='en',
            live=True)
        mock_suggestion.return_value = 'tuition'
        mock_filter.count.return_value = 5
        mock_filter.return_value = mock_queryset(count=5)
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
