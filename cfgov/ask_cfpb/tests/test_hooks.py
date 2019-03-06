from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import Client, TestCase

import mock

from ask_cfpb.models import Category, SubCategory
from ask_cfpb.models.pages import AnswerPage
from ask_cfpb.wagtail_hooks import (
    CategoryModelAdmin, SubCategoryModelAdmin, after_create_answer_page,
    editor_css
)
from v1.models import HomePage


django_client = Client()


class TestAskHooks(TestCase):

    def test_ask_hooks(self):
        self.assertEqual(SubCategoryModelAdmin.model, SubCategory)
        self.assertEqual(CategoryModelAdmin.model, Category)

    def test_js_functions(self):
        self.assertIn("css/question-tips.css", editor_css())


class TestFeedbackForm(TestCase):
    def new_page(self, slug):
        root = HomePage.objects.get(slug='cfgov')
        page = AnswerPage(
            title='test',
            slug=slug,
            live=False
        )
        root.add_child(instance=page)
        return page

    def test_feedback_form_gets_added_to_new_saved_answer_page(self):
        slug = 'test-answer-page-1'
        page = self.new_page(slug)
        page.save()
        request = mock.Mock()
        request.user = User.objects.last()
        after_create_answer_page(request, page)

        stream_data = page.content.stream_data
        feedback = filter(lambda item: item['type'] == 'feedback', stream_data)
        self.assertEquals(
            feedback[0]['value']['was_it_helpful_text'],
            'Was this page helpful to you?'
        )
        self.assertEquals(page.status_string, 'draft')

    def test_feedback_form_gets_added_to_new_published_answer_page(self):
        slug = 'test-answer-page-2'
        page = self.new_page(slug)
        page.save_revision().publish()
        request = mock.Mock()
        request.user = User.objects.last()
        request.POST = {'action-publish': 'action-publish'}
        after_create_answer_page(request, page)

        # Check that the published revision has the feedback form
        page = AnswerPage.objects.get(slug=slug)

        stream_data = page.content.stream_data
        feedback = filter(lambda item: item['type'] == 'feedback', stream_data)
        self.assertEquals(
            feedback[0]['value']['was_it_helpful_text'],
            'Was this page helpful to you?'
        )
        self.assertEquals(page.status_string, 'live')
