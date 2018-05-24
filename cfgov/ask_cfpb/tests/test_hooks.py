from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase

import mock

from ask_cfpb.wagtail_hooks import (
    Answer, AnswerModelAdmin, AnswerModelAdminSaveUserEditView, Audience,
    AudienceModelAdmin, Category, CategoryModelAdmin, NextStep,
    NextStepModelAdmin, SubCategory, SubCategoryModelAdmin, editor_css,
    editor_js, whitelister_element_rules
)


class TestAskHooks(TestCase):

    def test_ask_hooks(self):
        self.assertEqual(AnswerModelAdmin.model, Answer)
        self.assertEqual(AudienceModelAdmin.model, Audience)
        self.assertEqual(NextStepModelAdmin.model, NextStep)
        self.assertEqual(SubCategoryModelAdmin.model, SubCategory)
        self.assertEqual(AudienceModelAdmin.model, Audience)
        self.assertEqual(CategoryModelAdmin.model, Category)

    def test_js_functions(self):
        self.assertIn("registerHalloPlugin('editHtmlButton')", editor_js())
        self.assertIn("css/question_tips.css", editor_css())
        self.assertIn('aside', whitelister_element_rules().keys())
        self.assertIn('table', whitelister_element_rules().keys())

    def test_AnswerModelAdminSaveUserEditView(self):
        mock_admin = mock.Mock()
        mock_admin.is_page = True
        mock_admin.model = Answer
        mock_answer = Answer.objects.create(id=98765)
        mock_user = User(username='Goliath')
        mock_user.save()
        mock_request = HttpRequest()
        mock_request.user = mock_user
        mock_request.method = "GET"
        mock_edit_view = AnswerModelAdminSaveUserEditView(mock_admin, '98765')
        mock_edit_view.request = mock_request
        mock_edit_view.instance = mock_answer
        mock_edit_view.dispatch(mock_request)
        self.assertEqual(mock_answer.last_user.username, 'Goliath')
