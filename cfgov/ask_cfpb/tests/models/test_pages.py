from __future__ import unicode_literals
import HTMLParser

import json
import mock
from mock import patch
from model_mommy import mommy

from bs4 import BeautifulSoup as bs

from django.utils import timezone
from django.apps import apps
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.test import Client
from django.utils import html

from v1.util.migrations import get_or_create_page, get_free_path
from ask_cfpb.models.django import (
    Answer, Category, SubCategory, Audience,
    NextStep, ENGLISH_PARENT_SLUG, SPANISH_PARENT_SLUG)
from ask_cfpb.models.pages import (
    AnswerPage, AnswerCategoryPage)

html_parser = HTMLParser.HTMLParser()
client = Client()
now = timezone.now()


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

    def setUp(self):
        from v1.models import HomePage
        ROOT_PAGE = HomePage.objects.get(slug='cfgov')
        self.audience = mommy.make(Audience, name='stub_audience')
        self.category = mommy.make(Category, name='stub_cat', name_es='que')
        self.subcategories = mommy.make(
            SubCategory, name='stub_subcat', _quantity=3)
        self.category.subcategories.add(self.subcategories[0])
        self.category.save()
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
        self.answer1234 = self.prepare_answer(
            id=1234,
            answer='Mock answer 1',
            question='Mock question1')
        self.answer1234.save()
        self.page1 = self.create_answer_page()
        self.page1.answer_base = self.answer1234
        self.page1.parent = self.english_parent_page
        self.page1.save()
        self.answer5678 = self.prepare_answer(
            id=5678,
            answer='Mock answer 2',
            question='Mock question2')
        self.answer5678.save()
        self.page2 = self.create_answer_page(slug='mock-answer-page-en-5678')
        self.page2.answer_base = self.answer5678
        self.page2.parent = self.english_parent_page
        self.page2.save()

    def test_view_answer_200(self):
        response_200 = client.get(reverse(
            'ask-english-answer', args=['mock-answer-page', 'en', 1234]))
        self.assertTrue(isinstance(response_200, HttpResponse))
        self.assertEqual(response_200.status_code, 200)

    def test_view_answer_302(self):
        response_302 = client.get(reverse(
            'ask-english-answer', args=['mocking-answer-page', 'en', 1234]))
        self.assertTrue(isinstance(response_302, HttpResponse))
        self.assertEqual(response_302.status_code, 302)

    def test_view_answer_redirected(self):
        self.page1.redirect_to = self.page2.answer_base
        self.page1.save()
        response_302 = client.get(reverse(
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

    def test_spanish_template_used(self):
        spanish_answer = self.prepare_answer(
            answer_es='Spanish answer',
            slug_es='spanish-answer',
            update_spanish_page=True)
        spanish_answer.save()
        spanish_page = spanish_answer.spanish_page
        soup = bs(spanish_page.serve(HttpRequest()).rendered_content)
        self.assertIn('Oficina', soup.title.string)

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
        taglist = answer.tags()
        for name in ['Chutes', 'Ladders']:
            self.assertIn(name, taglist)

    def test_search_tags_es(self):
        """Test the list produced by answer.tags_es()"""
        answer = self.prepare_answer(search_tags_es='sistema judicial, tipos')
        answer.save()
        taglist = answer.tags_es()
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
        self.assertEqual(subcategory.__str__(), subcategory.name)

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
            test_page.status_string.lower(), "redirected but not live")
        test_page.live = True
        self.assertEqual(
            test_page.status_string.lower(), "redirected")
        test_page.redirect_to = None
        self.assertEqual(
            test_page.status_string.lower(), "live")

    def test_category_page_context(self):
        mock_site = mock.Mock()
        mock_site.hostname = 'localhost'
        mock_request = HttpRequest()
        mock_request.site = mock_site
        cat_page = self.create_category_page(ask_category=self.category)
        test_context = cat_page.get_context(mock_request)
        self.assertEqual(test_context['choices'][0][1], 'stub_subcat')

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
            test_context['audiences'].count(),
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

    def test_category_audience_json(self):
        self.answer1234.audiences.add(self.audience)
        self.answer1234.category.add(self.category)
        self.answer1234.save()
        self.assertEqual(
            self.category.audience_json,
            '{"stub_audience": ["1234"]}')

    def test_category_subcategory_json(self):
        self.answer1234.subcategory.add(self.subcategories[0])
        self.assertEqual(
            self.category.subcategory_json,
            '{"stub_subcat": ["1234"]}')

    def test_category_answer_json(self):
        self.answer1234.category.add(self.category)
        result_dict = json.loads(self.category.answer_json)
        self.assertEqual(result_dict.keys()[0], '1234')
        self.assertEqual(result_dict['1234']['url'], '/ask-cfpb/slug-en-1234')
        self.assertEqual(result_dict['1234']['question'], 'Mock question1')

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
