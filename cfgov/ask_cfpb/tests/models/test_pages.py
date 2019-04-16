# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import six
import unittest
from six.moves import html_parser as HTMLParser

from django.apps import apps
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import Http404, HttpRequest, HttpResponse
from django.template.defaultfilters import slugify
from django.test import RequestFactory, TestCase, override_settings
from django.utils import html, timezone, translation
from haystack.models import SearchResult
from haystack.query import SearchQuerySet

from wagtail.tests.utils import WagtailTestUtils

from model_mommy import mommy

from ask_cfpb.models.django import (
    ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG, Answer, Audience, Category,
    NextStep, SubCategory, generate_short_slug
)
from ask_cfpb.models.pages import (
    PORTAL_CATEGORY_SORT_ORDER, REUSABLE_TEXT_TITLES, AnswerCategoryPage,
    AnswerPage, PortalSearchPage, validate_page_number
)
from ask_cfpb.scripts.export_ask_data import (
    assemble_output, clean_and_strip, export_questions
)
from v1.models import (
    CFGOVImage, HomePage, PortalCategory, PortalTopic, SublandingPage
)
from v1.tests.wagtail_pages import helpers
from v1.util.migrations import get_free_path, get_or_create_page


if six.PY2:
    import mock  # pragma: no cover
else:
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


class AnswerSlugCreationTest(unittest.TestCase):

    def test_long_slug_string(self):
        long_string = (
            "This string is more than 100 characters long, I assure you. "
            "No, really, more than 100 characters loooong.")
        self.assertEqual(
            generate_short_slug(long_string),
            ('this-string-is-more-than-100-characters-long-'
             'i-assure-you-no-really-more-than-100-characters'))

    def test_short_slug_string(self):
        short_string = "This string is less than 100 characters long."
        self.assertEqual(
            generate_short_slug(short_string), slugify(short_string))

    def test_slug_string_that_will_end_with_a_hyphen(self):
        """
        It's possible for slug truncation to result in a slug that ends
        on a hypthen. In that case the function should strip the ending hyphen.
        """
        will_end_with_hyphen = (
            "This string is more than 100 characters long, I assure you. "
            "No, really, more than 100 characters looong and end on a hyphen.")
        self.assertEqual(
            generate_short_slug(will_end_with_hyphen),
            'this-string-is-more-than-100-characters-long-i-assure-you-'
            'no-really-more-than-100-characters-looong')


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
            'PortalCategories': "Subcat1 | Subcat2",
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


class PortalSearchPageTestCase(TestCase):

    fixtures = [
        'ask_tests', 'portal_topics', 'portal_categories', 'test_ask_tags'
    ]

    def setUp(self):
        self.ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.test_user = User.objects.last()
        self.factory = RequestFactory()
        self.english_parent = SublandingPage(
            title='Consumer Tools',
            slug='consumer-tools')
        self.ROOT_PAGE.add_child(instance=self.english_parent)
        self.english_parent.save()
        self.english_parent.save_revision(user=self.test_user).publish()
        self.english_page = PortalSearchPage(
            title="Auto loans",
            slug='answers')
        self.english_parent.add_child(instance=self.english_page)
        self.english_page.save()
        self.english_page.portal_topic_id = 1
        self.english_page.save_revision(user=self.test_user).publish()

        self.spanish_parent = SublandingPage(
            title='Obtener respuestas',
            slug='obtener-respuestas')
        self.ROOT_PAGE.add_child(instance=self.spanish_parent)
        self.spanish_parent.save()
        self.spanish_parent.save_revision(user=self.test_user).publish()
        self.spanish_page = PortalSearchPage(
            title="Préstamos para vehículos",
            language='es',
            slug='respuestas')
        self.spanish_parent.add_child(instance=self.spanish_page)
        self.spanish_page.save()
        self.spanish_page.portal_topic_id = 1
        self.spanish_page.save_revision(user=self.test_user).publish()

    def test_get_english_topic_heading(self):
        page = self.english_page
        self.assertEqual(page.get_heading(), 'Auto loans')

    def test_get_english_category_heading(self):
        page = self.english_page
        page.portal_category = PortalCategory.objects.get(
            heading='How-to guides')
        self.assertEqual(page.get_heading(), 'How-to guides')

    def test_get_spanish_topic_heading(self):
        page = self.spanish_page
        self.assertEqual(
            page.get_heading(), 'Préstamos para vehículos')

    def test_get_spanish_category_heading(self):
        page = self.spanish_page
        page.portal_category = PortalCategory.objects.get(
            heading_es='Paso a paso')
        self.assertEqual(
            page.get_heading(), 'Paso a paso')

    def test_english_portal_title(self):
        test_page = PortalSearchPage(
            title="Auto loans",
            slug="auto-loans")
        self.english_parent.add_child(instance=test_page)
        test_page.save()
        test_page.portal_topic_id = 1
        test_page.save_revision(user=self.test_user).publish()
        self.assertEqual(str(test_page), test_page.title)
        self.assertEqual(test_page.portal_topic, PortalTopic.objects.get(pk=1))

    def test_category_map_length(self):
        self.assertEqual(
            len(self.english_page.category_map),
            PortalCategory.objects.count())

    def test_category_map_sort_order(self):
        mapping = self.english_page.category_map
        self.assertEqual(
            PORTAL_CATEGORY_SORT_ORDER,
            [category.pk for slug, category in mapping.items()]
        )

    def test_results_message_no_category_no_search_term(self):
        msg = self.english_page.results_message(10, 'Auto loans', '')
        self.assertEqual(msg, "Showing 10 results  within auto loans")

    def test_results_message_no_category_with_search_term(self):
        msg = self.english_page.results_message(1, 'Auto loans', 'hoodoo')
        self.assertEqual(
            msg, 'Showing  1 result for "hoodoo" within auto loans')

    def test_results_message_with_category_no_search_term(self):
        self.english_page.portal_category = PortalCategory.objects.get(
            heading='How-to guides')
        msg = self.english_page.results_message(10, 'How-to guides', '')
        self.assertEqual(msg, "Showing 10 results within how-to guides")

    def test_results_message_with_category_and_search_term(self):
        self.english_page.portal_category = PortalCategory.objects.get(
            heading='How-to guides')
        msg = self.english_page.results_message(1, 'How-to guides', 'hoodoo')
        self.assertEqual(
            msg,
            '<p>Showing  1 result for &quot;hoodoo&quot; within how-to guides'
            '</p><p><a href="../?search_term=hoodoo">'
            'See all results within auto loans</a></p>')

    def test_portal_topic_page_200(self):
        page = self.english_page
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.filter')
    def test_portal_category_page_200(self, mock_filter):
        mock_filter.return_value = mock_queryset(count=2)
        page = self.english_page
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
        page = self.spanish_page
        response = self.client.get(page.url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.filter')
    # @mock.patch('ask_cfpb.models.pages.SearchQuerySet.count')
    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.spelling_suggestion')
    def test_portal_topic_page_with_no_hits_same_suggestion(
            self, mock_suggestion, mock_filter):
        mock_suggestion.return_value = 'hoodoo'
        mock_filter.return_value = mock_queryset()
        page = self.english_page
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
        page = self.english_page
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
        page = self.english_page
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
        page = self.english_page
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
        page = self.english_page
        url = "{}?search_term=hoodoo".format(page.url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['search_term'], 'hoodoo')


class AnswerPageTestCase(TestCase):

    def prepare_answer(self, **kwargs):
        kwargs.setdefault('answer', 'Mock answer')
        kwargs.setdefault('slug', 'mock-answer')
        return mommy.prepare(Answer, **kwargs)

    def create_answer_page(self, **kwargs):
        kwargs.setdefault(
            'path', get_free_path(apps, self.english_parent_page))
        kwargs.setdefault('depth', self.english_parent_page.depth + 1)
        kwargs.setdefault('slug', 'mock-answer-page-en-1234')
        kwargs.setdefault('title', 'Mock answer page title')
        page = mommy.prepare(AnswerPage, **kwargs)
        page.save()
        return page

    def create_category_page(self, **kwargs):
        kwargs.setdefault(
            'path', get_free_path(apps, self.english_parent_page))
        kwargs.setdefault('depth', self.english_parent_page.depth + 1)
        kwargs.setdefault('slug', 'category-mortgages')
        kwargs.setdefault('title', 'Mortgages')
        kwargs.setdefault('language', 'en')
        cat_page = AnswerCategoryPage(**kwargs)
        self.english_parent_page.add_child(instance=cat_page)
        cat_page.save()
        return cat_page

    def create_es_category_page(self, **kwargs):
        kwargs.setdefault('slug', 'spanishcat')
        kwargs.setdefault('title', 'Spanish mortgages')
        kwargs.setdefault('language', 'es')
        es_cat_page = AnswerCategoryPage(**kwargs)
        self.spanish_parent_page.add_child(instance=es_cat_page)
        es_cat_page.save()
        return es_cat_page

    def setUp(self):
        self.test_user = User.objects.last()
        self.factory = RequestFactory()
        ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.audience = mommy.make(Audience, name='stub_audience')
        self.category = mommy.make(
            Category, name='stub_cat', name_es='que', slug='stub-cat')
        self.subcategories = mommy.make(
            SubCategory, name='stub_subcat', parent=self.category, _quantity=3)
        self.category.subcategories.add(self.subcategories[0])
        self.category.save()
        self.test_image = mommy.make(CFGOVImage)
        self.test_image2 = mommy.make(CFGOVImage)
        self.next_step = mommy.make(NextStep, title='stub_step')
        page_clean = mock.patch('ask_cfpb.models.pages.CFGOVPage.clean')
        page_clean.start()
        self.addCleanup(page_clean.stop)
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
        self.answer1234 = self.prepare_answer(
            id=1234,
            answer='Mock answer 1',
            answer_es='Mock Spanish answer',
            slug='mock-answer-en-1234',
            slug_es='mock-spanish-answer-es-1234',
            question='Mock question1',
            question_es='Mock Spanish question1',
            search_tags='hippodrome',
            search_tags_es='hipotecas',
            update_english_page=True,
            update_spanish_page=True)
        self.answer1234.save()
        self.page1 = AnswerPage(
            language='en',
            answer_base=self.answer1234,
            slug='mock-question-en-1234',
            title='Mock question1',
            answer='Mock answer 1',
            question='Mock question1',
            search_tags='hippodrome')
        self.english_parent_page.add_child(instance=self.page1)
        self.page1.save_revision().publish()
        self.page1_es = AnswerPage(
            language='es',
            slug='mock-spanish-question1-es-1234',
            title='Mock Spanish question1',
            answer_base=self.answer1234,
            answer='Mock Spanish answer',
            question='Mock Spanish question1',
            search_tags='hipotecas')
        self.spanish_parent_page.add_child(instance=self.page1_es)
        self.page1_es.save_revision().publish()
        self.answer5678 = self.prepare_answer(
            id=5678,
            answer='Mock answer 2',
            question='Mock question2',
            search_tags='hippodrome',
            search_tags_es='hipotecas')
        self.answer5678.save()
        self.page2 = AnswerPage(
            language='en',
            slug='mock-question2-en-5678',
            title='Mock question2',
            answer_base=self.answer5678,
            answer='Mock answer 2',
            question='Mock question2',
            search_tags='hippodrome')
        self.english_parent_page.add_child(instance=self.page2)
        self.page2.save_revision().publish()

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

    def test_routable_category_page_view(self):
        cat_page = self.create_category_page(
            ask_category=self.category)
        response = cat_page.serve(HttpRequest())
        self.assertEqual(response.status_code, 200)

    def test_es_routable_category_page_view(self):
        es_cat_page = self.create_es_category_page(
            ask_category=self.category)
        response = es_cat_page.serve(HttpRequest())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(es_cat_page.language, 'es')
        self.assertEqual(es_cat_page.get_language_display(), 'Spanish')
        self.assertEqual(
            es_cat_page.template, 'ask-cfpb/category-page.html')

    def test_routable_category_page_bad_pagination(self):
        cat_page = self.create_category_page(
            ask_category=self.category)
        request = HttpRequest()
        request.GET['page'] = 50
        response = cat_page.serve(HttpRequest())
        self.assertEqual(response.status_code, 200)

    def test_routable_category_page_invalid_pagination(self):
        cat_page = self.create_category_page(
            ask_category=self.category)
        request = HttpRequest()
        request.GET['page'] = 'A50'
        response = cat_page.serve(HttpRequest())
        self.assertEqual(response.status_code, 200)

    def test_routable_subcategory_page_view(self):
        cat_page = self.create_category_page(
            ask_category=self.category)
        response = cat_page.subcategory_page(
            HttpRequest(), subcat=self.subcategories[0].slug)
        self.assertEqual(response.status_code, 200)

    def test_routable_subcategory_page_bad_subcategory(self):
        cat_page = self.create_category_page(
            ask_category=self.category)
        with self.assertRaises(Http404):
            cat_page.subcategory_page(HttpRequest(), subcat=None)

    def test_routable_subcategory_page_bad_pagination(self):
        cat_page = self.create_category_page(
            ask_category=self.category)
        request = HttpRequest()
        request.GET['page'] = 100
        response = cat_page.subcategory_page(
            request, subcat=self.subcategories[0].slug)
        self.assertEqual(response.status_code, 200)

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

    def test_category_text(self):
        answer = self.prepare_answer()
        answer.save()
        answer.category.add(self.category)
        answer.save()
        self.assertEqual(answer.category_text(), [self.category.name])
        self.assertEqual(answer.category_text_es(), [self.category.name_es])

    def test_category_text_no_category(self):
        answer = self.prepare_answer()
        answer.save()
        self.assertEqual(answer.category_text(), '')
        self.assertEqual(answer.category_text_es(), '')

    def test_answer_text(self):
        raw_snippet = "<strong>Snippet</strong>."
        raw_answer = "<span>Clean answer test&nbsp;</span>"
        combo = "{} {}".format(raw_snippet, raw_answer)
        clean = html.strip_tags(html_parser.unescape(combo)).strip()
        answer = self.prepare_answer(
            snippet=raw_snippet,
            answer=raw_answer,
            snippet_es=raw_snippet,
            answer_es=raw_answer)
        answer.save()
        self.assertEqual(answer.answer_text, clean)
        self.assertEqual(answer.answer_text_es, clean)

    def test_cleaned_questions(self):
        answer = self.prepare_answer(
            question="<span>Clean question test&nbsp;</span>",
            question_es="<span>Clean question test&nbsp;</span>")
        raw = "<span>Clean question test&nbsp;</span>"
        clean = html.strip_tags(html_parser.unescape(raw)).strip()
        answer.save()
        self.assertEqual(answer.cleaned_questions(), [clean])
        self.assertEqual(answer.cleaned_questions_es(), [clean])

    def test_answer_str(self):
        answer = self.prepare_answer(question="Let's test an English slug")
        answer.save()
        self.assertEqual(
            answer.__str__(),
            answer.question)

    def test_answer_str_no_english_question(self):
        answer = self.prepare_answer(
            question='',
            question_es="Let's test with no English")
        answer.save()
        self.assertEqual(
            answer.__str__(),
            answer.question_es)

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

    def test_category_featured_answers(self):
        category = self.category
        page = self.page1
        page.category.add(category)
        page.featured = True
        page.save_revision().publish()
        category.save()
        self.assertIn(page, category.featured_answers('en'))

    def test_subcategory_str(self):
        subcategory = self.subcategories[0]
        self.assertEqual(
            subcategory.__str__(),
            "{}: {}".format(self.category.name, subcategory.name))

    def test_nextstep_str(self):
        next_step = self.next_step
        self.assertEqual(next_step.__str__(), next_step.title)

    def test_audience_str(self):
        audience = self.audience
        self.assertEqual(audience.__str__(), audience.name)

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

    def test_get_ask_nav_items(self):
        from ask_cfpb.models import get_ask_nav_items
        mommy.make(Category, name='test_cat')
        test_nav_items = get_ask_nav_items({}, self.page1)[0]
        self.assertEqual(
            len(test_nav_items),
            Category.objects.count())

    def test_get_es_ask_nav_items(self):
        from ask_cfpb.models import get_ask_nav_items
        mommy.make(Category, name='test_es_cat')
        test_nav_items = get_ask_nav_items({}, self.page1_es)[0]
        self.assertEqual(
            len(test_nav_items),
            Category.objects.count())

    def test_get_ask_breadcrumbs(self):
        from ask_cfpb.models import get_ask_breadcrumbs
        breadcrumbs = get_ask_breadcrumbs()
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs[0]['title'], 'Ask CFPB')

    def test_get_ask_breadcrumbs_with_category(self):
        from ask_cfpb.models import get_ask_breadcrumbs
        test_category = mommy.make(Category, name='breadcrumb_cat')
        breadcrumbs = get_ask_breadcrumbs(category=test_category)
        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs[0]['title'], 'Ask CFPB')
        self.assertEqual(breadcrumbs[1]['title'], test_category.name)

    def test_get_es_ask_breadcrumbs_with_category(self):
        from ask_cfpb.models import get_ask_breadcrumbs
        test_category = mommy.make(Category, name_es='es_breadcrumb_cat')
        breadcrumbs = get_ask_breadcrumbs(
            language='es', category=test_category)
        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs[0]['title'], 'Obtener respuestas')
        self.assertEqual(breadcrumbs[1]['title'], test_category.name_es)

    def test_category_page_context(self):
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        cat_page = self.create_category_page(ask_category=self.category)
        test_context = cat_page.get_context(mock_request)
        self.assertEqual(
            test_context['choices'].count(),
            self.category.subcategories.count())

    def test_landing_page_context(self):
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        landing_page = self.english_parent_page
        test_context = landing_page.get_context(mock_request)
        self.assertEqual(
            test_context['categories'].count(),
            Category.objects.count())

    def test_category_page_add_js_function(self):
        cat_page = self.create_category_page(ask_category=self.category)
        self.assertEqual(cat_page.page_js, ['secondary-navigation.js'])

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

    def test_category_meta_image_undefined(self):
        """ Category page's meta image is undefined if the category has
        no image
        """
        category_page = self.create_category_page(ask_category=self.category)
        self.assertIsNone(category_page.meta_image)

    def test_social_sharing_image_used(self):
        from v1.models.images import CFGOVImage
        image = CFGOVImage.objects.last()
        page = self.page1
        page.social_sharing_image = image
        page.save_revision(user=self.test_user).publish()
        self.assertEqual(page.meta_image, image)

    def test_category_meta_image_uses_category_image(self):
        """ Category page's meta image is its category's image """
        category = mommy.make(Category, category_image=self.test_image)
        category_page = self.create_category_page(ask_category=category)
        self.assertEqual(category_page.meta_image, self.test_image)

    def test_answer_meta_image_undefined(self):
        """ Answer page's meta image is undefined if social image is
        not provided
        """
        answer = self.prepare_answer()
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

    def test_answer_page_context_collects_subcategories(self):
        """ Answer page's context delivers all related subcategories """
        page = self.page1
        page.category.add(self.category)
        related_subcat = mommy.make(
            SubCategory,
            name='related_subcat',
            parent=self.category)
        subcat1 = self.subcategories[0]
        subcat1.related_subcategories.add(related_subcat)
        for each in self.subcategories:
            page.subcategory.add(each)
        page.save_revision()
        request = HttpRequest()
        context = page.get_context(request)
        self.assertEqual(len(context['subcategories']), 4)

    def test_answer_page_context_collects_subcategories_with_same_parent(self):
        """ Answer page's context delivers only subcategories that
            share the selected parent category """
        page = self.page1
        test_category = mommy.make(
            Category, name='Test cat', slug='test-cat')
        test_subcategory = mommy.make(
            SubCategory, name='test_subcat', parent=test_category)
        test_category.subcategories.add(test_subcategory)
        page.category.add(test_category)
        page.subcategory.add(test_subcategory)
        page.category.add(self.category)
        for each in self.subcategories:
            page.subcategory.add(each)
        page.save_revision()
        request = HttpRequest()
        context = page.get_context(request)
        first_category = page.category.first()
        self.assertEqual(context['category'], first_category)
        self.assertEqual(len(context['subcategories']),
                         first_category.subcategories.count())

    def test_answer_page_breadcrumbs_and_subcategories(self):
        """ If there is no referrer, category/breadcrumbs should reflect
        first category on answer."""
        page = self.page1
        test_category = mommy.make(
            Category, name='Test cat', slug='test-cat')
        page.category.add(self.category)
        page.category.add(test_category)
        request = HttpRequest()
        request.META['HTTP_REFERER'] = ''
        context = page.get_context(request)
        default_category = page.category.first()
        self.assertEqual(context['category'], default_category)
        self.assertEqual(len(context['breadcrumb_items']), 2)
        self.assertEqual(context['breadcrumb_items'][1]['title'],
                         default_category.name)

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
