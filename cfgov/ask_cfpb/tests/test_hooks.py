from __future__ import unicode_literals

from django.test import TestCase

from ask_cfpb.models import Audience, Category, NextStep, SubCategory
from ask_cfpb.wagtail_hooks import (
    AudienceModelAdmin, CategoryModelAdmin, NextStepModelAdmin,
    SubCategoryModelAdmin, editor_css
)


class TestAskHooks(TestCase):

    def test_ask_hooks(self):
        self.assertEqual(AudienceModelAdmin.model, Audience)
        self.assertEqual(NextStepModelAdmin.model, NextStep)
        self.assertEqual(SubCategoryModelAdmin.model, SubCategory)
        self.assertEqual(AudienceModelAdmin.model, Audience)
        self.assertEqual(CategoryModelAdmin.model, Category)

    def test_js_functions(self):
        self.assertIn("css/question-tips.css", editor_css())
