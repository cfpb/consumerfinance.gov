from __future__ import unicode_literals

import HTMLParser

from django.utils import html
from django.test import TestCase
import mock
from mock import patch
from model_mommy import mommy

from django.apps import apps
from wagtail.wagtailcore.models import Page

from v1.util.migrations import get_or_create_page
from ask_cfpb.models.django import (
    Answer, Category, SubCategory, Audience, NextStep, PARENT_SLUG)
from ask_cfpb.models.pages import AnswerPage

html_parser = HTMLParser.HTMLParser()


class AnswerModelTestCase(TestCase):
    def setUp(self):
        self.audiences = [mommy.make(Audience, name='stub_audience')]
        self.category = mommy.make(Category, name='stub_cat')
        self.subcategories = mommy.make(
            SubCategory, name='stub_subcat', _quantity=3)
        self.next_step = mommy.make(NextStep, title='stub_step')
        page_clean = patch('ask_cfpb.models.pages.CFGOVPage.clean')
        page_clean.start()
        self.addCleanup(page_clean.stop)
        self.parent_page = get_or_create_page(
            apps,
            'v1',
            'LandingPage',
            'Ask CFPB',
            PARENT_SLUG,
            Page.objects.get(slug='cfgov'),
            live=True)

    def prepare_answer(self, **kwargs):
        kwargs.setdefault('answer', 'Mock answer')
        kwargs.setdefault('slug', 'mock-answer')
        return mommy.prepare(Answer, **kwargs)

    def create_answer_page(self, **kwargs):
        kwargs.setdefault('path', 001)
        kwargs.setdefault('depth', 3)
        kwargs.setdefault('slug', 'mock-answer-page')
        kwargs.setdefault('title', 'Mock answer page title')
        page = mommy.prepare(AnswerPage, **kwargs)
        page.save()
        return page

    def test_answer_deletion(self):
        """deleting an answer should also delete its related pages"""
        answer = self.prepare_answer(
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

    def test_available_subcategories(self):
        parent_category = self.category
        for sc in self.subcategories:
            sc.parent = parent_category
            sc.save()
        answer = self.prepare_answer()
        answer.save()
        answer.category.add(parent_category)
        answer.save()
        self.assertEqual(answer.available_subcategories, self.subcategories)

    def test_subcat_slugs(self):
        answer = self.prepare_answer()
        answer.save()
        for sc in self.subcategories:
            answer.subcategory.add = sc
        answer.save()
        self.assertEqual(
            answer.subcat_slugs(),
            [cat.slug for cat in answer.subcategory.all()])

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

    def test_tagging(self):
        """Test the generator produced by answer.tags()"""
        answer = self.prepare_answer(tagging='Chutes, Ladders')
        answer.save()
        taglist = [tag for tag in answer.tags()]
        for name in ['Chutes', 'Ladders']:
            self.assertIn(name, taglist)

    def test_category_text(self):
        answer = self.prepare_answer()
        answer.save()
        answer.category.add(self.category)
        answer.save()
        self.assertEqual(answer.category_text(), [self.category.name])

    def test_category_text_no_category(self):
        answer = self.prepare_answer()
        answer.save()
        self.assertEqual(answer.category_text(), '')

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
        self.assertEqual(answer.answer_text(), clean)
        self.assertEqual(answer.answer_text_es(), clean)

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

    def test_subcategory_str(self):
        subcategory = self.subcategories[0]
        self.assertEqual(subcategory.__str__(), subcategory.name)

    def test_nextstep_str(self):
        next_step = self.next_step
        self.assertEqual(next_step.__str__(), next_step.title)

    def test_audience_str(self):
        audience = self.audiences[0]
        self.assertEqual(audience.__str__(), audience.name)
