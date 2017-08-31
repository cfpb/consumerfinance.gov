from __future__ import unicode_literals
import datetime
import HTMLParser

import json
import mock
from mock import mock_open, patch
from model_mommy import mommy
import unittest

from bs4 import BeautifulSoup as bs

from django.apps import apps
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponse, Http404
from django.template.defaultfilters import slugify
from django.test import TestCase
from django.utils import html
from django.utils import timezone
from django.utils.translation import ugettext as _

from v1.models import CFGOVImage
from v1.util.migrations import get_or_create_page, get_free_path
from ask_cfpb.models.django import (
    Answer, Audience, Category, generate_short_slug, NextStep,
    SubCategory, ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG)
from ask_cfpb.models.pages import (
    AnswerPage, AnswerCategoryPage, AnswerAudiencePage)
from ask_cfpb.scripts.export_ask_data import (
    assemble_output, clean_and_strip, export_questions)

html_parser = HTMLParser.HTMLParser()
now = timezone.now()


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


class OutputScriptFunctionTests(unittest.TestCase):

    def setUp(self):
        self.mock_assemble_output_value = [{
            'ASK_ID': 123456,
            'Question': "Question",
            'ShortAnswer': "Short answer.",
            'Answer': "Long answer.",
            'URL': "fakeurl.com",
            'SpanishQuestion': "Spanish question.",
            'SpanishAnswer': "Spanish answer",
            'SpanishURL': "fakespanishurl.com",
            'Topic': "Category 5 Hurricane",
            'SubCategories': "Subcat1 | Subcat2",
            'Audiences': "Audience1 | Audience2",
            'RelatedQuestions': "1 | 2 | 3",
            'RelatedResources': "Owning a Home"}]

    def test_clean_and_strip(self):
        raw_data = "<p>If you have been scammed, file a complaint.</p>"
        clean_data = "If you have been scammed, file a complaint."
        self.assertEqual(clean_and_strip(raw_data), clean_data)

    @mock.patch('ask_cfpb.scripts.export_ask_data.assemble_output')
    def test_export_questions(self, mock_output):
        mock_output.return_value = self.mock_assemble_output_value
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        slug = 'ask-cfpb-{}.csv'.format(timestamp)
        m = mock_open()
        with patch('__builtin__.open', m, create=True):
            export_questions()
        self.assertEqual(mock_output.call_count, 1)
        m.assert_called_once_with("/tmp/{}".format(slug), 'w')


class AnswerModelTestCase(TestCase):

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
        page = mommy.prepare(AnswerCategoryPage, **kwargs)
        page.save()
        return page

    def create_audience_page(self, **kwargs):
        kwargs.setdefault(
            'path', get_free_path(apps, self.english_parent_page))
        kwargs.setdefault('depth', self.english_parent_page.depth + 1)
        kwargs.setdefault('slug', 'audience-students')
        kwargs.setdefault('title', 'Students')
        page = mommy.prepare(AnswerAudiencePage, **kwargs)
        page.save()
        return page

    def setUp(self):
        from v1.models import HomePage
        ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.audience = mommy.make(Audience, name='stub_audience')
        self.category = mommy.make(Category, name='stub_cat', name_es='que')
        self.subcategories = mommy.make(
            SubCategory, name='stub_subcat', parent=self.category, _quantity=3)
        self.category.subcategories.add(self.subcategories[0])
        self.category.save()
        self.test_image = mommy.make(CFGOVImage)
        self.test_image2 = mommy.make(CFGOVImage)
        self.next_step = mommy.make(NextStep, title='stub_step')
        page_clean = patch('ask_cfpb.models.pages.CFGOVPage.clean')
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
        self.page1 = self.answer1234.english_page
        self.page1_es = self.answer1234.spanish_page
        self.answer5678 = self.prepare_answer(
            id=5678,
            answer='Mock answer 2',
            question='Mock question2',
            search_tags='hippodrome',
            search_tags_es='hipotecas')
        self.answer5678.save()
        self.page2 = self.create_answer_page(slug='mock-answer-page-en-5678')
        self.page2.answer_base = self.answer5678
        self.page2.parent = self.english_parent_page
        self.page2.save()

    def test_export_script_assemble_output(self):
        expected_urls = ['/ask-cfpb/mock-question1-en-1234/',
                         '/ask-cfpb/mock-answer-page-en-5678/']
        expected_questions = ['Mock question1', 'Mock question2']
        test_output = assemble_output()
        for obj in test_output:
            self.assertIn(obj.get('ASK_ID'), [1234, 5678])
            self.assertIn(obj.get('URL'), expected_urls)
            self.assertIn(obj.get('Question'), expected_questions)

    def test_spanish_print_page(self):
        response = self.client.get(reverse(
            'ask-spanish-print-answer',
            args=['slug', 'es', '1234']))
        self.assertEqual(response.status_code, 200)

    def test_spanish_print_page_no_answer_404(self):
        response = self.client.get(reverse(
            'ask-spanish-print-answer',
            args=['slug', 'es', '9999']))
        self.assertEqual(response.status_code, 404)

    def test_spanish_page_print_blank_answer_404(self):
        test_answer = self.prepare_answer(
            id=999,
            answer_es='',
            slug_es='mock-spanish-answer-es-999',
            question_es='Mock Spanish question1',
            update_spanish_page=True)
        test_answer.save()
        response = self.client.get(reverse(
            'ask-spanish-print-answer',
            args=['slug', 'es', 999]))
        self.assertEqual(response.status_code, 404)

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

    def test_english_page_get_template(self):
        page = self.page1
        self.assertEqual(
            page.get_template(HttpRequest()),
            'ask-cfpb/answer-page.html')

    def test_facet_map(self):
        self.answer1234.category.add(self.category)
        self.answer1234.audiences.add(self.audience)
        self.answer1234.subcategory.add(self.subcategories[1])
        facet_map = self.category.facet_map
        self.assertEqual(
            json.loads(facet_map)['answers']['1234']['question'],
            'Mock question1')
        self.assertEqual(
            json.loads(facet_map)['audiences']['1']['name'],
            'stub_audience')
        self.assertEqual(
            json.loads(facet_map)['subcategories']['1'], [])

    def test_answer_valid_tags(self):
        test_dict = Answer.valid_tags()
        self.assertIn('hippodrome', test_dict['valid_tags'])

    def test_answer_valid_es_tags(self):
        test_dict = Answer.valid_tags(language='es')
        self.assertIn('hipotecas', test_dict['valid_tags'])

    def test_answer_invalid_tag(self):
        test_dict = Answer.valid_tags(language='es')
        self.assertNotIn('hippopotamus', test_dict['valid_tags'])

    def test_routable_category_page_view(self):
        cat_page = self.create_category_page(
            ask_category=self.category)
        response = cat_page.category_page(HttpRequest())
        self.assertEqual(response.status_code, 200)

    def test_routable_category_page_bad_pagination(self):
        cat_page = self.create_category_page(
            ask_category=self.category)
        request = HttpRequest()
        request.GET['page'] = 50
        response = cat_page.category_page(request)
        self.assertEqual(response.status_code, 200)

    def test_routable_category_page_invalid_pagination(self):
        cat_page = self.create_category_page(
            ask_category=self.category)
        request = HttpRequest()
        request.GET['page'] = 'A50'
        response = cat_page.category_page(request)
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

    def test_routable_tag_page_en_template(self):
        page = self.tag_results_page_en
        self.assertEqual(
            page.get_template(HttpRequest()),
            'ask-cfpb/answer-search-results.html')

    def test_routable_tag_page_es_template(self):
        page = self.tag_results_page_es
        self.assertEqual(
            page.get_template(HttpRequest()),
            'ask-cfpb/answer-tag-spanish-results.html')

    def test_routable_tag_page_base_returns_404(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_base'))
        self.assertEqual(response.status_code, 404)

    def test_routable_tag_page_es_bad_tag_returns_404(self):
        page = self.tag_results_page_es
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_search',
                kwargs={'tag': 'hippopotamus'}))
        self.assertEqual(response.status_code, 404)

    def test_routable_tag_page_en_bad_tag_returns_404(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_search',
                kwargs={'tag': 'hippopotamus'}))
        self.assertEqual(response.status_code, 404)

    def test_routable_tag_page_es_handles_bad_pagination(self):
        page = self.tag_results_page_es
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_search',
                kwargs={'tag': 'hipotecas'}), {'page': '100'})
        self.assertEqual(response.status_code, 200)

    def test_routable_tag_page_en_handles_bad_pagination(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_search',
                kwargs={'tag': 'hippodrome'}), {'page': '100'})
        self.assertEqual(response.status_code, 200)

    def test_routable_tag_page_es_valid_tag_returns_200(self):
        page = self.tag_results_page_es
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_search',
                kwargs={'tag': 'hipotecas'}))
        self.assertEqual(response.status_code, 200)

    def test_routable_tag_page_en_valid_tag_returns_200(self):
        page = self.tag_results_page_en
        response = self.client.get(
            page.url + page.reverse_subpage(
                'tag_search',
                kwargs={'tag': 'hippodrome'}))
        self.assertEqual(response.status_code, 200)

    def test_routable_tag_page_es_returns_url_suffix(self):
        page = self.tag_results_page_es
        response = page.reverse_subpage(
            'tag_search', kwargs={'tag': 'hipotecas'})
        self.assertEqual(response, 'hipotecas/')

    def test_routable_tag_page_en_returns_url_suffix(self):
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

    def test_view_answer_302_for_healed_slug(self):
        page = self.page1
        revision = page.save_revision()
        revision.publish()
        response = self.client.get(reverse(
            'ask-english-answer', args=['mock-slug', 'en', 1234]))
        self.assertEqual(response.status_code, 302)

    def test_view_answer_redirected(self):
        page = self.page1
        page.redirect_to = self.page2.answer_base
        page.save()
        revision = page.save_revision()
        revision.publish()
        response_302 = self.client.get(reverse(
            'ask-english-answer', args=['mocking-answer-page', 'en', 1234]))
        self.assertTrue(isinstance(response_302, HttpResponse))
        self.assertEqual(response_302.status_code, 302)

    def test_answer_deletion(self):
        """deleting an answer should also delete its related pages"""
        answer = self.prepare_answer(
            created_at=now,
            question='Mock question',
            question_es='Mock Spanish question',
            answer_es='Mock Spanish Answer.')
        answer.save()
        answer.create_or_update_pages()
        ID = answer.id
        self.assertEqual(Answer.objects.get(id=ID), answer)
        self.assertEqual(
            AnswerPage.objects.filter(answer_base=answer).count(), 2)
        answer.delete()
        self.assertEqual(
            AnswerPage.objects.filter(answer_base=answer).count(), 0)
        self.assertEqual(
            Answer.objects.filter(id=ID).count(), 0)

    def test_audience_page_add_js(self):
        test_page = self.create_audience_page(language='en')
        test_js = {'template': []}
        test_page.add_page_js(test_js)
        self.assertTrue(
            'secondary-navigation.js'
            in test_page.media['template'])

    def test_audience_page_add_js_wrong_language(self):
        """add_page_js should only work on English Audience pages"""
        test_page = self.create_audience_page(language='es')
        test_js = {'template': []}
        test_page.add_page_js(test_js)
        self.assertFalse(
            'secondary-navigation.js'
            in test_page.media['template'])

    def test_spanish_template_used(self):
        spanish_answer = self.prepare_answer(
            answer_es='Spanish answer',
            slug_es='spanish-answer',
            update_spanish_page=True)
        spanish_answer.save()
        spanish_page = spanish_answer.spanish_page
        soup = bs(spanish_page.serve(HttpRequest()).rendered_content)
        self.assertIn('Oficina', soup.title.string)

    def test_spanish_answer_page_handles_referrer_with_unicode_accents(self):
        referrer_unicode = (
            'https://www.consumerfinance.gov/es/obtener-respuestas/'
            'buscar-por-etiqueta/empresas_de_informes_de_cr\xe9dito/')
        spanish_answer = self.prepare_answer(
            answer_es='Spanish answer',
            slug_es='spanish-answer',
            update_spanish_page=True)
        spanish_answer.save()
        spanish_page = spanish_answer.spanish_page
        request = HttpRequest()
        request.POST['referrer'] = referrer_unicode
        response = spanish_page.serve(request)
        self.assertEqual(response.status_code, 200)

    def test_create_or_update_page_unsuppoted_language(self):
        answer = self.prepare_answer()
        answer.save()
        with self.assertRaises(ValueError):
            answer.create_or_update_page(language='zz')

    def test_create_or_update_pages_english_only(self):
        answer = self.prepare_answer()
        answer.save()
        result = answer.create_or_update_pages()
        self.assertEqual(result, 1)

    def test_create_or_update_pages_spanish_only(self):
        answer = self.prepare_answer(answer='', answer_es='vamos')
        answer.save()
        result = answer.create_or_update_pages()
        self.assertEqual(result, 1)

    def test_create_or_update_pages_both_languages(self):
        answer = self.prepare_answer(answer_es='vamos')
        answer.save()
        result = answer.create_or_update_pages()
        self.assertEqual(result, 2)

    @mock.patch('ask_cfpb.models.django.Answer.create_or_update_page')
    def test_save_skip_page_update(self, mock_create_page):
        answer = self.prepare_answer(
            question='Test question.',
            question_es='Test Spanish question.',
            answer_es='vamos',
            update_english_page=True,
            update_spanish_page=True)
        answer.save(skip_page_update=True)
        self.assertEqual(mock_create_page.call_count, 0)

    @mock.patch('ask_cfpb.models.django.Answer.create_or_update_page')
    def test_save_english_to_page(self, mock_create_page):
        answer = self.prepare_answer(
            question='Test question.',
            question_es='Test Spanish question.',
            answer_es='vamos',
            update_english_page=True,
            update_spanish_page=False)
        answer.save()
        mock_create_page.assert_called_with(language='en')
        self.assertEqual(mock_create_page.call_count, 1)

    @mock.patch('ask_cfpb.models.django.Answer.create_or_update_page')
    def test_save_spanish_to_page(self, mock_create_page):
        answer = self.prepare_answer(
            question='Test question.',
            question_es='Test Spanish question.',
            answer_es='vamos',
            update_english_page=False,
            update_spanish_page=True)
        answer.save()
        mock_create_page.assert_called_with(language='es')
        self.assertEqual(mock_create_page.call_count, 1)

    @mock.patch('ask_cfpb.models.django.Answer.create_or_update_page')
    def test_save_both_languages_to_page(self, mock_create_page):
        answer = self.prepare_answer(
            question='Test question.',
            question_es='Test Spanish question.',
            answer_es='vamos',
            update_english_page=True,
            update_spanish_page=True)
        answer.save()
        mock_create_page.assert_called_with(language='es')
        self.assertEqual(mock_create_page.call_count, 2)

    def test_has_live_page(self):
        answer = self.prepare_answer()
        answer.save()
        self.assertEqual(answer.has_live_page(), False)
        answer.update_english_page = True
        answer.save()
        _page = answer.answer_pages.get(language='en')
        self.assertEqual(answer.has_live_page(), False)
        _revision = _page.save_revision()
        _revision.publish()
        self.assertEqual(answer.has_live_page(), True)

    def test_available_subcategories_qs(self):
        parent_category = self.category
        for sc in self.subcategories:
            sc.parent = parent_category
            sc.save()
        answer = self.prepare_answer()
        answer.save()
        answer.category.add(parent_category)
        answer.save()
        for subcat in self.subcategories:
            self.assertIn(subcat, answer.available_subcategory_qs)

    def test_bass_string_no_base(self):  # sic
        test_page = self.create_answer_page()
        result = test_page.__str__()
        self.assertEqual(result, test_page.title)

    def test_bass_string_with_base(self):  # sic
        mock_answer = self.prepare_answer()
        mock_answer.save()
        test_page = self.create_answer_page(answer_base=mock_answer)
        result = test_page.__str__()
        self.assertEqual(result, "{}: {}".format(
            mock_answer.id, test_page.title))

    def test_audience_strings(self):
        """Test the generator produced by answer.audience_strings()"""
        audience = Audience.objects.first()
        answer = self.prepare_answer()
        answer.save()
        answer.audiences.add(audience)
        answer.save()
        self.assertIn(audience.name, answer.audience_strings())

    def test_search_tags(self):
        """Test the list produced by answer.tags()"""
        answer = self.prepare_answer(search_tags='Chutes, Ladders')
        answer.save()
        taglist = answer.tags
        for name in ['Chutes', 'Ladders']:
            self.assertIn(name, taglist)

    def test_search_tags_es(self):
        """Test the list produced by answer.tags_es()"""
        answer = self.prepare_answer(search_tags_es='sistema judicial, tipos')
        answer.save()
        taglist = answer.tags_es
        for term in ['sistema judicial', 'tipos']:
            self.assertIn(term, taglist)

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
            "{} {}".format(answer.id, answer.slug))

    def test_category_str(self):
        category = self.category
        self.assertEqual(category.__str__(), category.name)

    def test_category_featured_answers(self):
        category = self.category
        mock_answer = self.answer1234
        mock_answer.featured = True
        mock_answer.category.add(category)
        mock_answer.save()
        self.assertIn(mock_answer, category.featured_answers())

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
        answer1 = self.prepare_answer()
        answer1.save()
        answer2 = self.prepare_answer()
        answer2.save()
        test_page = self.create_answer_page(answer_base=answer1)
        test_page.live = False
        test_redirect_page = self.create_answer_page(answer_base=answer2)
        test_page.redirect_to = test_redirect_page.answer_base
        self.assertEqual(
            test_page.status_string.lower(),
            _("redirected but not live").lower())
        test_page.live = True
        self.assertEqual(
            test_page.status_string.lower(), _("redirected").lower())
        test_page.redirect_to = None
        self.assertEqual(
            test_page.status_string.lower(), _("live").lower())

    def test_get_ask_nav_items(self):
        from ask_cfpb.models import get_ask_nav_items
        mommy.make(Category, name='test_cat')
        test_nav_items = get_ask_nav_items({}, {})[0]
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
        breadcrumbs = get_ask_breadcrumbs(test_category)
        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs[0]['title'], 'Ask CFPB')
        self.assertEqual(breadcrumbs[1]['title'], test_category.name)

    def test_audience_page_get_english_template(self):
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        audience_page = self.create_audience_page(
            ask_audience=self.audience, language='en')
        test_get_template = audience_page.get_template(mock_request)
        self.assertEqual(
            test_get_template,
            'ask-cfpb/audience-page.html')

    def test_audience_page_context(self):
        from ask_cfpb.models import get_ask_nav_items
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        audience_page = self.create_audience_page(
            ask_audience=self.audience, language='en')
        test_context = audience_page.get_context(mock_request)
        self.assertEqual(
            test_context['get_secondary_nav_items'],
            get_ask_nav_items)

    def test_audience_page_handles_bad_pagination(self):
        audience_page = self.create_audience_page(
            ask_audience=self.audience, language='en')
        request = HttpRequest()
        request.GET['page'] = '100'
        response = audience_page.serve(request)
        self.assertEqual(response.status_code, 200)

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

    def test_category_page_truncation(self):
        answer = self.answer1234
        answer.answer_es = ("We need an answer with more than 40 words to"
                            "prove that truncation is working as expected."
                            "It just so happens that the standard maximum "
                            "length for a news story's lead graph is around "
                            "40 words, which I have now managed to exceed.")
        answer.category.add(self.category)
        answer.save()
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        cat_page = self.create_category_page(
            ask_category=self.category, language='es')
        test_context = cat_page.get_context(mock_request)
        self.assertTrue(
            test_context['answers'][0]['answer_es'].endswith('...'))

    def test_category_page_context_es(self):
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        cat_page = self.create_category_page(
            ask_category=self.category, language='es')
        test_context = cat_page.get_context(mock_request)
        self.assertEqual(
            test_context['choices'].count(),
            self.category.subcategories.count())

    @mock.patch('ask_cfpb.models.pages.SearchQuerySet.filter')
    def test_category_page_context_no_es(self, mock_es_query):
        mock_return_value = mock.Mock()
        mock_return_value.facet_map = json.dumps(
            {'answers': {},
             'audiences': {},
             'subcategories': {}})
        mock_es_query.return_value = [mock_return_value]
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        cat_page = self.create_category_page(ask_category=self.category)
        test_context = cat_page.get_context(mock_request)
        self.assertEqual(
            test_context['facet_map'],
            mock_return_value.facet_map)

    def test_category_page_get_english_template(self):
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        cat_page = self.create_category_page(
            ask_category=self.category, language='en')
        test_get_template = cat_page.get_template(mock_request)
        self.assertEqual(
            test_get_template,
            'ask-cfpb/category-page.html')

    def test_category_page_get_spanish_template(self):
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        cat_page = self.create_category_page(
            ask_category=self.category, language='es')
        test_get_template = cat_page.get_template(mock_request)
        self.assertEqual(
            test_get_template,
            'ask-cfpb/category-page-spanish.html')

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
        self.assertEqual(
            len(test_context['audiences']),
            Audience.objects.count())

    def test_landing_page_get_english_template(self):
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        landing_page = self.english_parent_page
        test_get_template = landing_page.get_template(mock_request)
        self.assertEqual(
            test_get_template,
            'ask-cfpb/landing-page.html')

    def test_landing_page_get_spanish_template(self):
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        landing_page = self.spanish_parent_page
        test_get_template = landing_page.get_template(mock_request)
        self.assertEqual(
            test_get_template,
            'ask-cfpb/landing-page-spanish.html')

    def test_category_page_add_js_function(self):
        cat_page = self.create_category_page(ask_category=self.category)
        js = {}
        cat_page.add_page_js(js)
        self.assertEqual(js, {'template': [u'secondary-navigation.js']})

    def test_answer_language_page_exists(self):
        self.assertEqual(self.answer5678.english_page, self.page2)

    def test_answer_language_page_nonexistent(self):
        self.assertEqual(self.answer5678.spanish_page, None)

    def test_answer_page_print_template_used(self):
        answer_page = self.create_answer_page(language='es')
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        mock_request.GET = {'print': 'true'}
        self.assertEqual(
            answer_page.get_template(mock_request),
            'ask-cfpb/answer-page-spanish-printable.html')

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

    def test_category_meta_image_undefined(self):
        """ Category page's meta image is undefined if the category has
        no image
        """
        category_page = self.create_category_page(ask_category=self.category)
        self.assertIsNone(category_page.meta_image)

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

    def test_answer_meta_image_uses_social_image(self):
        """ Answer page's meta image is its answer's social image """
        answer = self.prepare_answer(social_sharing_image=self.test_image)
        answer.save()
        page = self.create_answer_page(answer_base=answer)
        self.assertEqual(page.meta_image, self.test_image)

    def test_answer_meta_image_uses_category_image_if_no_social_image(self):
        """ Answer page's meta image is its category's image """
        category = mommy.make(Category, category_image=self.test_image)
        answer = self.prepare_answer()
        answer.save()
        answer.category.add(category)
        page = self.create_answer_page(answer_base=answer)
        self.assertEqual(page.meta_image, self.test_image)

    def test_answer_meta_image_uses_social_image_not_category_image(self):
        """ Answer page's meta image pulls from its social image instead
        of its category's image
        """
        category = mommy.make(Category, category_image=self.test_image)
        answer = self.prepare_answer(social_sharing_image=self.test_image2)
        answer.save()
        answer.category.add(category)
        page = self.create_answer_page(answer_base=answer)
        self.assertEqual(page.meta_image, self.test_image2)

    def test_answer_page_context_collects_subcategories(self):
        """ Answer page's context delivers all related subcategories """
        answer = self.answer1234
        answer.category.add(self.category)
        related_subcat = mommy.make(
            SubCategory,
            name='related_subcat',
            parent=self.category)
        subcat1 = self.subcategories[0]
        subcat1.related_subcategories.add(related_subcat)
        for each in self.subcategories:
            answer.subcategory.add(each)
        answer.update_english_page = True
        answer.save()
        page = answer.english_page
        request = HttpRequest()
        context = page.get_context(request)
        self.assertEqual(len(context['subcategories']), 4)

    def test_answer_page_context_collects_subcategories_with_same_parent(self):
        """ Answer page's context delivers only subcategories that
            share the selected parent category """
        answer = self.answer1234
        test_category = mommy.make(
            Category, name='Test cat', slug='test-cat')
        test_subcategory = mommy.make(
            SubCategory, name='test_subcat', parent=test_category)
        test_category.subcategories.add(test_subcategory)
        answer.category.add(test_category)
        answer.subcategory.add(test_subcategory)
        answer.category.add(self.category)
        for each in self.subcategories:
            answer.subcategory.add(each)
        answer.update_english_page = True
        answer.save()
        page = answer.english_page
        request = HttpRequest()
        context = page.get_context(request)
        first_category = answer.category.first()
        self.assertEqual(context['category'], first_category)
        self.assertEqual(len(context['subcategories']),
                         first_category.subcategories.count())

    def test_answer_page_breadcrumbs_and_subcategories_with_no_referrer(self):
        """ If there is no referrer, category/breadcrumbs should reflect
        first category on answer."""
        answer = self.answer1234
        test_category = mommy.make(
            Category, name='Test cat', slug='test-cat')
        answer.category.add(self.category)
        answer.category.add(test_category)
        page = answer.english_page
        request = HttpRequest()
        request.META['HTTP_REFERER'] = ''
        context = page.get_context(request)
        default_category = answer.category.first()
        self.assertEqual(context['category'], default_category)
        self.assertEqual(len(context['breadcrumb_items']), 2)
        self.assertEqual(context['breadcrumb_items'][1]['title'],
                         default_category.name)

    def test_answer_page_context_with_category_referrer(self):
        """ If the referrer is a category page and category is on answer,
        breadcrumbs should lead back to category page,
        context['category'] should be referring category, and subcategories
        should be any on answer from referring category."""
        answer = self.answer1234
        test_category = mommy.make(
            Category, name='Test cat', slug='test-cat')
        test_subcategory = mommy.make(
            SubCategory, name='test_subcat', parent=test_category)
        test_category.subcategories.add(test_subcategory)
        answer.category.add(test_category)
        answer.subcategory.add(test_subcategory)
        answer.category.add(self.category)
        for each in self.subcategories:
            answer.subcategory.add(each)
        page = answer.english_page
        request = HttpRequest()
        request.META['HTTP_REFERER'] = 'https://www.consumerfinance.gov/' \
            + 'ask-cfpb/category-' + test_category.slug + '/subcategory/'
        context = page.get_context(request)
        breadcrumbs = context['breadcrumb_items']
        self.assertEqual(len(breadcrumbs), 2)
        self.assertEqual(breadcrumbs[1]['title'], test_category.name)
        self.assertEqual(context['category'], test_category)
        self.assertEqual(len(context['subcategories']), 1)

    def test_answer_page_context_with_portal_referrer_and_category(self):
        """ If the referrer is a portal page and portal's related category
        appears on answer page, breadcrumbs should lead back to portal,
        category should be portal's related category, and subcategories
        should be any on answer from portal related category."""
        from ask_cfpb.models import CONSUMER_TOOLS_PORTAL_PAGES as portals
        portal_path = list(portals.keys())[0]
        data = portals[portal_path]
        portal_title = data[0]
        category_slug = data[1]
        test_category = mommy.make(
            Category, name="test", slug=category_slug)
        answer = self.answer1234
        answer.category.add(self.category)
        answer.category.add(test_category)
        page = answer.english_page
        request = HttpRequest()
        request.META['HTTP_REFERER'] = \
            'https://www.consumerfinance.gov' + portal_path
        context = page.get_context(request)
        breadcrumbs = context['breadcrumb_items']
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs[0]['title'], portal_title)
        self.assertEqual(breadcrumbs[0]['href'], portal_path)
        self.assertEqual(context['category'].slug, category_slug)

    def test_answer_context_with_portal_referrer_and_no_category(self):
        """ If the referrer is a portal page but portal's related category
        does not appear on answer page, breadcrumbs should lead back to portal
        but there should be no category or subcategories on context."""
        from ask_cfpb.models import CONSUMER_TOOLS_PORTAL_PAGES as portals
        portal_path = list(portals.keys())[0]
        portal_title = portals[portal_path][0]
        answer = self.answer1234
        answer.category.add(self.category)
        for each in self.subcategories:
            answer.subcategory.add(each)
        page = answer.english_page
        request = HttpRequest()
        request.META['HTTP_REFERER'] = \
            'https://www.consumerfinance.gov' + portal_path
        context = page.get_context(request)
        breadcrumbs = context['breadcrumb_items']
        self.assertEqual(len(breadcrumbs), 1)
        self.assertEqual(breadcrumbs[0]['title'], portal_title)
        self.assertEqual(breadcrumbs[0]['href'], portal_path)
        self.assertEqual(context['category'], None)
        self.assertEqual(context['subcategories'], set())
