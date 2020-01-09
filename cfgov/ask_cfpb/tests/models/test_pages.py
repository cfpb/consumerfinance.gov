# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import six
from six.moves import html_parser as HTMLParser

from django.apps import apps
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponse
from django.test import TestCase, override_settings
from django.utils import timezone, translation
from haystack.models import SearchResult
from haystack.query import SearchQuerySet

from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtailcore.blocks import StreamValue

from model_mommy import mommy

from ask_cfpb.models.django import (
    ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG, Answer, Category, NextStep
)
from ask_cfpb.models.pages import (
    REUSABLE_TEXT_TITLES, AnswerLandingPage, AnswerPage, ArticlePage,
    PortalSearchPage, get_standard_text, validate_page_number
)
from ask_cfpb.models.snippets import GlossaryTerm
from ask_cfpb.scripts.export_ask_data import (
    assemble_output, clean_and_strip, export_questions
)
from v1.models import (
    CFGOVImage, HomePage, PortalCategory, PortalTopic, SublandingPage
)
from v1.tests.wagtail_pages import helpers
from v1.util.migrations import get_free_path, get_or_create_page

from unittest import mock  # pragma: no cover

html_parser = HTMLParser.HTMLParser()
now = timezone.now()


class MockSearchResult(SearchResult):
    def __init__(self, app_label, model_name, pk, score, **kwargs):
        self.autocomplete = "What is mock question {}?".format(pk)
        self.url = "/ask-cfpb/mock-question-en-{}/".format(pk)
        self.text = "Mock answer text for question {}.".format(pk)
        super(MockSearchResult, self).__init__(  # pragma: no cover
            app_label, model_name, pk, score, **kwargs)


def mock_queryset(count=0):
    class MockSearchQuerySet(SearchQuerySet):
        def __iter__(self):
            if count:
                return iter([
                    MockSearchResult('ask_cfpb', 'AnswerPage', i, 0.5)
                    for i in list(range(1, count + 1))])
            else:
                return iter([])

        def count(self):
            return count

        def filter(self, *args, **kwargs):
            return self

        def models(self, *models):
            return self  # pragma: no cover

    return MockSearchQuerySet()


class AnswerStringTestCase(TestCase):

    def test_answer_string_method(self):
        test_answer = Answer(question="Test question?")
        test_answer.save()
        self.assertEqual(test_answer.__str__(), test_answer.question)


class ExportAskDataTests(TestCase, WagtailTestUtils):

    def setUp(self):
        self.mock_assemble_output_value = [{
            'ASK_ID': 123456,
            'PAGE_ID': 56789,
            'Question': "Question",
            'ShortAnswer': "Short answer.",
            'Answer': "Long answer.",
            'URL': "fakeurl.com",
            'PortalTopics': "Category 5 Hurricane",
            'RelatedQuestions': "1 | 2 | 3",
            'RelatedResources': "Owning a Home"}]

    def test_export_script_assemble_output(self):
        answer = Answer(id=1234)
        answer.save()
        page = AnswerPage(
            slug='mock-question1-en-1234',
            title='Mock question1')
        page.answer_base = answer
        page.question = 'Mock question1'
        page.answer_content = StreamValue(
            page.answer_content.stream_block, [{
                'type': 'text',
                'value': 'Mock answer'
            }], True
        )
        helpers.publish_page(page)

        output = assemble_output()[0]
        self.assertEqual(output.get('ASK_ID'), 1234)
        self.assertEqual(output.get('URL'), '/mock-question1-en-1234/')
        self.assertEqual(output.get('Question'), 'Mock question1')

    def test_clean_and_strip(self):
        raw_data = "<p>If you have been scammed, file a complaint.</p>"
        clean_data = "If you have been scammed, file a complaint."
        self.assertEqual(clean_and_strip(raw_data), clean_data)

    @mock.patch('ask_cfpb.scripts.export_ask_data.assemble_output')
    def test_export_questions(self, mock_output):
        mock_output.return_value = self.mock_assemble_output_value
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        slug = 'ask-cfpb-{}.csv'.format(timestamp)
        m = mock.mock_open()
        with mock.patch('six.moves.builtins.open', m, create=True):
            export_questions()
        self.assertEqual(mock_output.call_count, 1)
        m.assert_called_once_with("/tmp/{}".format(slug), 'w')

    @mock.patch('ask_cfpb.scripts.export_ask_data.assemble_output')
    def test_export_from_admin_post(self, mock_output):
        self.login()
        mock_output.return_value = self.mock_assemble_output_value
        response = self.client.post('/admin/export-ask/')
        self.assertEqual(response.status_code, 200)
        # Check that fields from the mock value are included
        self.assertContains(response, 'Category 5 Hurricane')
        self.assertContains(response, '56789')
        self.assertContains(response, 'fakeurl.com')

    def test_export_from_admin_get(self):
        self.login()
        response = self.client.get('/admin/export-ask/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Download a spreadsheet')


class ArticlePageTestCase(TestCase):

    fixtures = ['ask_tests']

    def setUp(self):

        def create_page(model, title, slug, parent, language='en', **kwargs):
            new_page = model(
                live=False,
                language=language,
                title=title,
                slug=slug)
            for k, v in kwargs.items():
                setattr(new_page, k, v)
            parent.add_child(instance=new_page)
            new_page.save()
            new_page.save_revision(user=self.test_user).publish()
            return new_page
        self.test_user = User.objects.last()
        self.ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.tools_parent = create_page(
            SublandingPage,
            'Consumer Tools',
            'consumer-tools',
            self.ROOT_PAGE)
        self.article_page = create_page(
            ArticlePage,
            'Article title',
            'article-title',
            self.tools_parent,
            category='basics',
            heading='Article heading',
            intro='Article itro.'
        )

    def test_article_page_str(self):
        self.assertEqual(
            self.article_page.title,
            "{}".format(self.article_page)
        )

    def test_article_page_response(self):
        response = self.client.get(self.article_page.url)
        self.assertEqual(
            response.status_code, 200)

    def test_article_page_context(self):
        response = self.client.get(self.article_page.url)
        self.assertEqual(
            get_standard_text(self.article_page.language, 'about_us'),
            response.context_data.get('about_us')
        )


class PortalSearchPageTestCase(TestCase):

    fixtures = [
        'ask_tests', 'portal_topics', 'portal_categories', 'test_ask_tags'
    ]

    def setUp(self):

        def create_page(model, title, slug, parent, language='en', **kwargs):
            new_page = model(
                live=False,
                language=language,
                title=title,
                slug=slug)
            for k, v in kwargs.items():
                setattr(new_page, k, v)
            parent.add_child(instance=new_page)
            new_page.save()
            new_page.save_revision(user=self.test_user).publish()
            return new_page
        self.portal_topic = PortalTopic.objects.get(pk=1)
        self.portal_topic2 = PortalTopic.objects.get(pk=2)
        self.ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.test_user = User.objects.last()
        self.english_ask_parent = create_page(
            AnswerLandingPage,
            'Ask CFPB',
            'ask-cfpb',
            self.ROOT_PAGE)
        self.english_portal_parent = create_page(
            SublandingPage,
            'Consumer Tools',
            'consumer-tools',
            self.ROOT_PAGE)
        self.english_portal = create_page(
            SublandingPage,
            'Auto loans',
            'auto-loans',
            self.english_portal_parent,
            portal_topic_id=1)
        self.english_portal2 = create_page(
            SublandingPage,
            'Bank accounts',
            'bank-accounts',
            self.english_portal_parent,
            portal_topic_id=2)
        self.english_search_page = create_page(
            PortalSearchPage,
            'Auto loan answers',
            'answers',
            self.english_portal,
            portal_topic_id=1)
        self.english_search_page2 = create_page(
            PortalSearchPage,
            'Bank account answers',
            'answers',
            self.english_portal2,
            portal_topic_id=2)
        self.spanish_parent = create_page(
            SublandingPage,
            'Obtener respuestas',
            'obtener-respuestas',
            self.ROOT_PAGE,
            language='es')
        self.spanish_portal = create_page(
            SublandingPage,
            'Préstamos para vehículos',
            'prestamos-para-vehiculos',
            self.spanish_parent,
            language='es',
            portal_topic_id=1)
        self.spanish_search_page = create_page(
            PortalSearchPage,
            'Préstamos para vehículos respuestas',
            'respuestas',
            self.spanish_portal,
            language='es',
            portal_topic_id=1)
        self.answer_page = create_page(
            AnswerPage,
            'English auto-loans question-8888?',
            'english-auto-loans-question-en-8888',
            self.english_ask_parent,
            featured=True,
        )
        self.answer_page.portal_topic.add(self.portal_topic)
        self.answer_page.save()
        self.answer_page2 = create_page(
            AnswerPage,
            'English banks question-8889?',
            'english-banks-question-en-8889',
            self.english_ask_parent,
            featured=True,
        )
        self.answer_page.portal_topic.add(self.portal_topic2)
        self.answer_page.save()
        self.answer_page_es = create_page(
            AnswerPage,
            'Spanish test question-es-9999?',
            'spanish_test-question-es-9999',
            self.spanish_parent,
            language='es',
            primary_portal_topic_id=1,
        )

    def test_bad_category_value_raises_404(self):
        page = self.english_search_page
        url = page.url + page.reverse_subpage(
            'portal_category_page', kwargs={'category': 'how-to-gui'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_ask_breadcrumbs_with_portal(self):
        response = self.client.get(self.answer_page_es.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context_data['breadcrumb_items']), 1)
        self.assertEqual(
            response.context_data['breadcrumb_items'][0]['title'],
            self.answer_page_es.primary_portal_topic.heading_es)

    def test_get_ask_breadcrumbs_with_draft_portal(self):
        self.spanish_portal.unpublish()
        self.spanish_portal.save()
        response = self.client.get(self.answer_page_es.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context_data['breadcrumb_items']), 1)
        self.assertEqual(
            response.context_data['breadcrumb_items'][0]['title'],
            self.spanish_search_page.title)
        self.spanish_portal.save_revision(user=self.test_user).publish()

    def test_get_english_topic_heading(self):
        page = self.english_search_page
        self.assertEqual(page.get_heading(), 'Auto loans')

    def test_get_english_category_heading(self):
        page = self.english_search_page
        page.portal_category = PortalCategory.objects.get(
            heading='How-to guides')
        self.assertEqual(page.get_heading(), 'How-to guides')

    def test_get_spanish_topic_heading(self):
        page = self.spanish_search_page
        self.assertEqual(
            page.get_heading(), 'Préstamos para vehículos')

    def test_get_spanish_category_heading(self):
        page = self.spanish_search_page
        page.portal_category = PortalCategory.objects.get(
            heading_es='Paso a paso')
        self.assertEqual(
            page.get_heading(), 'Paso a paso')

    def test_english_portal_title(self):
        test_page = self.english_search_page
        self.assertEqual(str(test_page), test_page.title)
        self.assertEqual(test_page.portal_topic, PortalTopic.objects.get(pk=1))

    def test_english_category_title(self):
        page = self.english_search_page
        url = page.url + page.reverse_subpage(
            'portal_category_page', kwargs={'category': 'how-to-guides'})
        response = self.client.get(url)
        self.assertEqual(
            response.context_data.get('page').title,
            'Auto loans how-to guides')

    def test_spanish_category_title(self):
        page = self.spanish_search_page
        url = page.url + page.reverse_subpage(
            'portal_category_page', kwargs={'category': 'paso-a-paso'})
        response = self.client.get(url)
        self.assertEqual(
            response.context_data.get('page').title,
            'Préstamos para vehículos paso a paso')

    def test_category_map_length(self):
        self.assertEqual(
            len(self.english_search_page.category_map),
            PortalCategory.objects.count())

    def test_category_map_sort_order(self):
        mapping = self.english_search_page.category_map
        self.assertEqual(
            [p.pk for p in PortalCategory.objects.all()],
            [category.pk for slug, category in mapping.items()]
        )

    def test_results_message_no_category_no_search_term(self):
        msg = self.english_search_page.results_message(10, 'Auto loans', '')
        self.assertEqual(msg, "Showing 10 results  within auto loans")

    def test_results_message_no_category_with_search_term(self):
        msg = self.english_search_page.results_message(
            1, 'Auto loans', 'hoodoo')
        self.assertEqual(
            msg, 'Showing  1 result for "hoodoo" within auto loans')

    def test_results_message_with_category_no_search_term(self):
        self.english_search_page.portal_category = PortalCategory.objects.get(
            heading='How-to guides')
        msg = self.english_search_page.results_message(10, 'How-to guides', '')
        self.assertEqual(msg, "Showing 10 results within how-to guides")

    def test_results_message_with_category_and_search_term(self):
        self.english_search_page.portal_category = PortalCategory.objects.get(
            heading='How-to guides')
        msg = self.english_search_page.results_message(
            1, 'How-to guides', 'hoodoo')
        self.assertEqual(
            msg,
            'Showing  1 result for &quot;hoodoo&quot; within how-to guides'
            '<span class="results-link"><a href="../?search_term=hoodoo">'
            'See all results within auto loans</a></span>')

    def test_portal_topic_page_200(self):
        page = self.english_search_page
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.filter')
    def test_portal_category_page_200(self, mock_filter):
        mock_filter.return_value = mock_queryset(count=2)
        page = self.english_search_page
        url = page.url + page.reverse_subpage(
            'portal_category_page', kwargs={'category': 'how-to-guides'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('ask_cfpb.models.pages.PortalSearchPage.get_nav_items')
    def test_spanish_portal_search_page_200(self, mock_nav):
        mock_nav.return_value = [{
            'title': 'Spanish topic heading',
            'url': "mock-url",
            'active': False,
            'expanded': True,
            'children': []
        }], True
        page = self.spanish_search_page
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.filter')
    # @mock.patch('ask_cfpb.models.pages.SearchQuerySet.count')
    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.spelling_suggestion')
    def test_portal_topic_page_with_no_hits_same_suggestion(
            self, mock_suggestion, mock_filter):
        mock_suggestion.return_value = 'hoodoo'
        mock_filter.return_value = mock_queryset()
        page = self.english_search_page
        base_url = page.url
        url = "{}?search_term=hoodoo".format(base_url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.filter')
    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.count')
    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.spelling_suggestion')
    def test_portal_topic_page_with_no_hits_with_suggestion(
            self, mock_suggestion, mock_count, mock_filter):
        mock_suggestion.return_value = 'hoodunit'
        mock_count.return_value = 0
        mock_filter.return_value = mock_queryset()
        page = self.english_search_page
        base_url = page.url
        url = "{}?search_term=hoodoo".format(base_url)
        with override_settings(
                FLAGS={'ASK_SEARCH_TYPOS': [('boolean', True)]}):
            response = self.client.get(url)
            self.assertEqual(response.context_data['search_term'], 'hoodunit')
            self.assertEqual(response.status_code, 200)

    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.filter')
    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.count')
    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.spelling_suggestion')
    def test_portal_category_page_with_no_hits_with_suggestion(
            self, mock_suggestion, mock_count, mock_filter):
        mock_count.return_value = 0
        mock_suggestion.return_value = 'hoodunit'
        mock_filter.return_value = mock_queryset()
        page = self.english_search_page
        base_url = page.url + page.reverse_subpage(
            'portal_category_page', kwargs={'category': 'how-to-guides'})
        url = "{}?search_term=hoodoo".format(base_url)
        with override_settings(
                FLAGS={'ASK_SEARCH_TYPOS': [('boolean', True)]}):
            response = self.client.get(url)
            self.assertEqual(response.context_data['search_term'], 'hoodunit')
            self.assertEqual(response.status_code, 200)

    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.filter')
    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.count')
    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.spelling_suggestion')
    def test_portal_category_page_same_suggestion(
            self, mock_suggestion, mock_count, mock_filter):
        mock_filter.return_value = mock_queryset()
        mock_count.return_value = 0
        mock_suggestion.return_value = 'hoodoo'
        page = self.english_search_page
        base_url = page.url + page.reverse_subpage(
            'portal_category_page', kwargs={'category': 'how-to-guides'})
        url = "{}?search_term=hoodoo".format(base_url)
        response = self.client.get(url)
        self.assertEqual(response.context_data['search_term'], 'hoodoo')
        self.assertEqual(response.status_code, 200)

    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.models')
    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.filter')
    def test_portal_topic_page_suggestion(self, mock_filter, mock_models):
        mock_models.spelling_suggestion.return_value = 'hoodunit'
        mock_filter.return_value = mock_queryset()
        page = self.english_search_page
        url = "{}?search_term=hoodoo".format(page.url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['search_term'], 'hoodoo')

    def test_get_glossary_terms(self):
        page = self.english_search_page
        glossary_term = GlossaryTerm(
            name_en='Escrow',
            definition_en='Definition',
            portal_topic=page.portal_topic)
        glossary_term.save()
        terms = page.get_glossary_terms()
        self.assertEqual(next(terms).name('en'), 'Escrow')

    def test_portal_category_page_key_terms(self):
        page = self.english_search_page
        glossary_term = GlossaryTerm(
            name_en='Amortization',
            definition_en='Definition',
            portal_topic=page.portal_topic)
        glossary_term.save()
        url = "{}key-terms/".format(page.url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amortization')

    def test_portal_category_page_key_terms_spanish(self):
        page = self.spanish_search_page
        glossary_term = GlossaryTerm(
            name_en='Amortization',
            name_es='Amortización',
            definition_es='Definición',
            portal_topic=page.portal_topic)
        glossary_term.save()
        url = "{}palabras-claves/".format(page.url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amortización')

    def test_landing_page_live_portal(self):
        self.assertEqual(
            len(self.english_ask_parent.get_portal_cards()), 2
        )

    def test_landing_page_draft_portal(self):
        self.english_portal.unpublish()
        self.assertFalse(self.english_portal.live)
        self.english_ask_parent.refresh_from_db()
        self.assertEqual(
            len(self.english_ask_parent.get_portal_cards()), 2
        )

    def test_landing_page_draft_portals(self):
        for sl_page in SublandingPage.objects.all():
            sl_page.unpublish()
        self.assertEqual(
            len(self.english_ask_parent.get_portal_cards()), 2
        )

    def test_landing_page_draft_portals_draft_search(self):
        for sl_page in SublandingPage.objects.all():
            sl_page.unpublish()
        for s_page in self.portal_topic.portal_search_pages.all():
            s_page.unpublish()
        for s_page in self.portal_topic2.portal_search_pages.all():
            s_page.unpublish()
        self.assertEqual(self.english_ask_parent.get_portal_cards(), [])


class AnswerPageTestCase(TestCase):

    fixtures = ['ask_tests', 'portal_topics']

    def create_answer_page(self, **kwargs):
        kwargs.setdefault(
            'path', get_free_path(apps, self.english_parent_page))
        kwargs.setdefault('depth', self.english_parent_page.depth + 1)
        kwargs.setdefault('slug', 'mock-answer-page-en-1234')
        kwargs.setdefault('title', 'Mock answer page title')
        page = mommy.prepare(AnswerPage, **kwargs)
        page.save()
        return page

    def setUp(self):
        self.test_user = User.objects.get(pk=1)
        ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.category = mommy.make(
            Category, name='stub_cat', name_es='que', slug='stub-cat')
        self.category.save()
        self.test_image = mommy.make(CFGOVImage)
        self.test_image2 = mommy.make(CFGOVImage)
        self.next_step = mommy.make(NextStep, title='stub_step')
        self.portal_topic = mommy.make(
            PortalTopic,
            heading='test topic',
            heading_es='prueba tema')
        page_clean = mock.patch('ask_cfpb.models.pages.CFGOVPage.clean')
        page_clean.start()
        self.addCleanup(page_clean.stop)
        self.portal_page = SublandingPage(
            title='test portal page',
            slug='test-portal-page',
            portal_topic=self.portal_topic,
            language='en'
        )
        ROOT_PAGE.add_child(instance=self.portal_page)
        self.portal_page.save()
        self.portal_page.save_revision().publish()
        self.portal_page_es = SublandingPage(
            title='test portal page',
            slug='test-portal-page-es',
            portal_topic=self.portal_topic,
            language='es'
        )
        ROOT_PAGE.add_child(instance=self.portal_page_es)
        self.portal_page_es.save()
        self.portal_page_es.save_revision().publish()
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
        self.tag_results_page_en = get_or_create_page(
            apps,
            'ask_cfpb',
            'TagResultsPage',
            'Tag results page',
            'search-by-tag',
            ROOT_PAGE,
            language='en',
            live=True)
        self.tag_results_page_es = get_or_create_page(
            apps,
            'ask_cfpb',
            'TagResultsPage',
            'Tag results page',
            'buscar-por-etiqueta',
            ROOT_PAGE,
            language='es',
            live=True)
        self.answer1234 = Answer(id=1234)
        self.answer1234.save()
        self.page1 = AnswerPage(
            language='en',
            answer_base=self.answer1234,
            slug='mock-question-en-1234',
            title='Mock question1',
            answer_content='Mock answer 1',
            question='Mock question1',
            search_tags='hippodrome')
        self.english_parent_page.add_child(instance=self.page1)
        self.page1.save_revision().publish()
        self.page1_es = AnswerPage(
            language='es',
            slug='mock-spanish-question1-es-1234',
            title='Mock Spanish question1',
            answer_base=self.answer1234,
            answer_content='Mock Spanish answer',
            question='Mock Spanish question1',
            search_tags='hipotecas')
        self.spanish_parent_page.add_child(instance=self.page1_es)
        self.page1_es.save_revision().publish()
        self.answer5678 = Answer(id=5678)
        self.answer5678.save()
        self.page2 = AnswerPage(
            language='en',
            slug='mock-question2-en-5678',
            title='Mock question2',
            answer_base=self.answer5678,
            answer_content='Mock answer 2',
            question='Mock question2',
            search_tags='hippodrome')
        self.english_parent_page.add_child(instance=self.page2)
        self.page2.save_revision().publish()

    def test_tag_results_page_templates(self):
        self.assertEqual(
            self.tag_results_page_es.get_template(HttpRequest()),
            self.tag_results_page_en.get_template(HttpRequest()))

    def test_tag_results_page_context_language(self):
        context = self.tag_results_page_es.get_context(HttpRequest())
        self.assertEqual(
            context.get('breadcrumb_items')[0]['title'],
            'Obtener respuestas')

    def test_english_page_context(self):
        from v1.models.snippets import ReusableText
        from ask_cfpb.models.pages import get_reusable_text_snippet
        rt = ReusableText(title='About us (For consumers)')
        rt.save()
        page = self.page1
        page.language = 'en'
        page.save()
        test_context = page.get_context(HttpRequest())
        self.assertEqual(
            test_context['about_us'],
            get_reusable_text_snippet('About us (For consumers)'))

    def test_english_page_sibling_url(self):
        self.assertEqual(
            self.page1.get_sibling_url(),
            self.page1_es.url
        )

    def test_spanish_page_sibling_url(self):
        self.assertEqual(
            self.page1_es.get_sibling_url(),
            self.page1.url
        )

    def test_no_sibling_url_returned_for_redirected_page(self):
        self.page1_es.redirect_to_page = self.page2
        self.page1_es.save()
        self.page1_es.save_revision(user=self.test_user).publish()
        self.assertEqual(
            self.page1.get_sibling_url(),
            None
        )

    def test_no_sibling_url_returned_for_draft_page(self):
        self.page1.unpublish()
        self.assertEqual(
            self.page1_es.get_sibling_url(),
            None
        )

    def test_routable_tag_page_base_returns_404(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_base'))
        self.assertEqual(response.status_code, 404)

    def test_routable_tag_page_handles_bad_tag(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_search',
                kwargs={'tag': 'hippopotamus'}))
        self.assertEqual(response.status_code, 200)

    def test_routable_tag_page_handles_bad_pagination(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_search',
                kwargs={'tag': 'hippodrome'}), {'page': '100'})
        self.assertEqual(response.status_code, 200)

    def test_routable_tag_page_valid_tag_returns_200(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_search',
                kwargs={'tag': 'hippodrome'}))
        self.assertEqual(response.status_code, 200)

    def test_routable_tag_page_returns_url_suffix(self):
        page = self.tag_results_page_en
        response = page.reverse_subpage(
            'tag_search', kwargs={'tag': 'hippodrome'})
        self.assertEqual(response, 'hippodrome/')

    def test_view_answer_exact_slug(self):
        page = self.page1
        page.slug = 'mock-answer-en-1234'
        page.save()
        revision = page.save_revision()
        revision.publish()
        response = self.client.get(reverse(
            'ask-english-answer', args=['mock-answer', 'en', 1234]))
        self.assertEqual(response.status_code, 200)

    def test_view_answer_301_for_healed_slug(self):
        page = self.page1
        revision = page.save_revision()
        revision.publish()
        response = self.client.get(reverse(
            'ask-english-answer', args=['mock-slug', 'en', 1234]))
        self.assertEqual(response.status_code, 301)

    def test_view_answer_redirected(self):
        page = self.page1
        page.redirect_to = self.page2.answer_base
        page.save()
        revision = page.save_revision()
        revision.publish()
        response_302 = self.client.get(reverse(
            'ask-english-answer', args=['mocking-answer-page', 'en', 1234]))
        self.assertTrue(isinstance(response_302, HttpResponse))
        self.assertEqual(response_302.status_code, 301)

    def test_spanish_answer_page_handles_referrer_with_unicode_accents(self):
        referrer_unicode = (
            'https://www.consumerfinance.gov/es/obtener-respuestas/'
            'buscar-por-etiqueta/empresas_de_informes_de_cr\xe9dito/')
        spanish_page = self.page1_es
        request = HttpRequest()
        request.POST['referrer'] = referrer_unicode
        response = spanish_page.serve(request)
        self.assertEqual(response.status_code, 200)

    def test_page_string_no_base(self):
        test_page = self.create_answer_page()
        result = test_page.__str__()
        self.assertEqual(result, test_page.title)

    def test_page_string_with_base(self):
        page = self.page1
        self.assertTrue(page.answer_base)
        result = page.__str__()
        self.assertEqual(result, "{}: {}".format(
            page.answer_base.pk, page.title))

    def test_search_tags(self):
        """Test the list produced by page.clean_search_tags()"""
        page = self.page1
        page.search_tags = 'Chutes, Ladders'
        page.save_revision().publish()
        taglist = page.clean_search_tags
        for name in ['Chutes', 'Ladders']:
            self.assertIn(name, taglist)

    def test_english_header_and_footer(self):
        english_answer_page_response = self.client.get(reverse(
            'ask-english-answer',
            args=['mock-question', 'en', 1234]))
        self.assertContains(
            english_answer_page_response,
            'An official website of the United States government')
        self.assertNotContains(
            english_answer_page_response,
            'Un sitio web oficial del gobierno federal de los Estados Unidos')
        self.assertContains(
            english_answer_page_response,
            'https://usa.gov/')
        self.assertNotContains(
            english_answer_page_response,
            'https://gobiernousa.gov/')

    def test_spanish_header_and_footer(self):
        spanish_answer_page_response = self.client.get(reverse(
            'ask-spanish-answer',
            args=['mock-spanish-question1', 'es', 1234]))
        self.assertContains(
            spanish_answer_page_response,
            'Un sitio web oficial del gobierno federal de los Estados Unidos'
        )
        self.assertNotContains(
            spanish_answer_page_response,
            'An official website of the United States government'
        )
        self.assertContains(
            spanish_answer_page_response,
            'https://gobiernousa.gov/')
        self.assertNotContains(
            spanish_answer_page_response,
            'https://usa.gov/')

    def test_category_str(self):
        category = self.category
        self.assertEqual(category.__str__(), category.name)

    def test_portal_topic_featured_answers(self):
        page = self.page1
        page.portal_topic.add(self.portal_topic)
        page.featured = True
        page.save_revision().publish()
        self.assertIn(page, self.portal_topic.featured_answers('en'))

    def test_nextstep_str(self):
        next_step = self.next_step
        self.assertEqual(next_step.__str__(), next_step.title)

    def test_status_string(self):
        with translation.override('en'):
            page1 = self.page1
            self.assertEqual(
                (page1.status_string),
                'live + draft')

    def test_status_string_redirected(self):
        with translation.override('en'):
            page1 = self.page1
            page1.redirect_to_page = self.page2
            page1.save()
            page1.get_latest_revision().publish()
            self.assertEqual(
                (page1.status_string),
                "redirected")
            page1.unpublish()
            self.assertEqual(
                page1.status_string, ("redirected but not live"))

    def test_get_ask_breadcrumbs(self):
        from ask_cfpb.models import get_ask_breadcrumbs
        breadcrumbs = get_ask_breadcrumbs()
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs[0]['title'], 'Ask CFPB')

    def test_landing_page_context_no_featured_answer(self):
        page = self.page1
        page.portal_topic.add(self.portal_topic)
        page.featured = False
        page.save_revision().publish()
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        landing_page = self.english_parent_page
        test_context = landing_page.get_context(mock_request)
        self.assertEqual(len(test_context['portal_cards']), 0)

    def test_landing_page_context(self):
        page = self.page1
        page.portal_topic.add(self.portal_topic)
        page.featured = True
        page.save_revision().publish()
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        landing_page = self.english_parent_page
        test_context = landing_page.get_context(mock_request)
        self.assertEqual(len(test_context['portal_cards']), 1)
        self.assertEqual(
            test_context['portal_cards'][0]['title'],
            'test topic')

    def test_spanish_landing_page_context(self):
        page = self.page1_es
        page.portal_topic.add(self.portal_topic)
        page.featured = True
        page.save_revision().publish()
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        landing_page = self.spanish_parent_page
        test_context = landing_page.get_context(mock_request)
        self.assertEqual(len(test_context['portal_cards']), 1)
        self.assertEqual(
            test_context['portal_cards'][0]['title'],
            'prueba tema')

    def test_landing_page_context_draft_portal_page(self):
        page = self.page1
        page.portal_topic.add(self.portal_topic)
        page.featured = True
        page.save_revision().publish()
        self.portal_page.unpublish()
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        landing_page = self.english_parent_page
        test_context = landing_page.get_context(mock_request)
        self.assertEqual(len(test_context['portal_cards']), 0)

    def test_answer_language_page_exists(self):
        self.assertEqual(self.answer5678.english_page, self.page2)

    def test_answer_language_page_nonexistent(self):
        self.assertEqual(self.answer5678.spanish_page, None)

    def test_get_reusable_text_snippet(self):
        from ask_cfpb.models import get_reusable_text_snippet
        from v1.models.snippets import ReusableText
        test_snippet = ReusableText.objects.create(title='Test Snippet')
        self.assertEqual(
            get_reusable_text_snippet('Test Snippet'),
            test_snippet)

    def test_get_nonexistent_reusable_text_snippet(self):
        from ask_cfpb.models import get_reusable_text_snippet
        self.assertEqual(
            get_reusable_text_snippet('Nonexistent Snippet'),
            None)

    def test_get_about_us_english_standard_text(self):
        from ask_cfpb.models import get_standard_text
        from v1.models.snippets import ReusableText
        snippet_title = REUSABLE_TEXT_TITLES['about_us']['en']
        test_snippet = ReusableText.objects.create(title=snippet_title)
        self.assertEqual(
            get_standard_text('en', 'about_us'),
            test_snippet)

    def test_social_sharing_image_used(self):
        from v1.models.images import CFGOVImage
        image = CFGOVImage.objects.last()
        page = self.page1
        page.social_sharing_image = image
        page.save_revision(user=self.test_user).publish()
        self.assertEqual(page.meta_image, image)

    def test_answer_meta_image_undefined(self):
        """ Answer page's meta image is undefined if social image is
        not provided
        """
        answer = Answer()
        answer.save()
        page = self.create_answer_page(answer_base=answer)
        self.assertIsNone(page.meta_image)

    def test_answer_meta_image_uses_category_image_if_no_social_image(self):
        """ Answer page's meta image is its category's image """
        category = mommy.make(Category, category_image=self.test_image)
        page = self.page1
        page.category.add(category)
        page.save_revision()
        self.assertEqual(page.meta_image, self.test_image)

    def test_answer_split_testing_id(self):
        """Confirm AnswerPage's split_testing_id is set to its answer_base.id,
        which is checked by the core.feature_flags.in_split_testing_cluster
        flag condition when doing split testing on Ask CFPB answer pages."""
        answer = self.answer1234
        page = answer.english_page
        self.assertEqual(page.split_test_id, answer.id)

    def test_validate_pagination_number(self):
        paginator = Paginator([{'fake': 'results'}] * 30, 25)
        request = HttpRequest()
        self.assertEqual(validate_page_number(request, paginator), 1)
        request.GET.update({'page': '2'})
        self.assertEqual(validate_page_number(request, paginator), 2)
        request = HttpRequest()
        request.GET.update({'page': '1000'})
        self.assertEqual(validate_page_number(request, paginator), 1)
        request = HttpRequest()
        request.GET.update({'page': '<script>Boo</script>'})
        self.assertEqual(validate_page_number(request, paginator), 1)

    def test_schema_html_does_not_appear_when_flag_is_off(self):
        with override_settings(
                FLAGS={'HOW_TO_SCHEMA': [('boolean', False)]}):
            response = self.client.get(self.page1.url)
            self.assertNotContains(
                response,
                'itemtype="http://schema.org/HowTo"'
            )

    def test_schema_html_appears_when_flag_is_on(self):
        with override_settings(
                FLAGS={'HOW_TO_SCHEMA': [('boolean', True)]}):
            response = self.client.get(self.page1.url)
            self.assertContains(response, 'itemtype="http://schema.org/HowTo"')
