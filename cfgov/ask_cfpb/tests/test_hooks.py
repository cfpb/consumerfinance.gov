from __future__ import unicode_literals

from django.test import TestCase

from ask_cfpb.models import Category, SubCategory
from ask_cfpb.wagtail_hooks import (
    CategoryModelAdmin, SubCategoryModelAdmin, editor_css
)


class TestAskHooks(TestCase):

    def test_ask_hooks(self):
        self.assertEqual(SubCategoryModelAdmin.model, SubCategory)
        self.assertEqual(CategoryModelAdmin.model, Category)

    def test_js_functions(self):
        self.assertIn("css/question-tips.css", editor_css())
