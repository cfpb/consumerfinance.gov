from __future__ import unicode_literals

from unittest import TestCase

from ask_cfpb.wagtail_hooks import (
    Answer,
    AnswerModelAdmin,
    Audience,
    AudienceModelAdmin,
    NextStep,
    NextStepModelAdmin,
    SubCategory,
    SubCategoryModelAdmin,
    Category,
    CategoryModelAdmin,
    editor_js,
    editor_css,
    whitelister_element_rules)


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
        self.assertEqual(whitelister_element_rules().keys(), ['aside'])
