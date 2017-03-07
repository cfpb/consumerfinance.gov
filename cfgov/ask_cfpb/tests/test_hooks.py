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
    CategoryModelAdmin)


class TestAskHooks(TestCase):

    def test_ask_hooks(self):
        self.assertEqual(AnswerModelAdmin.model, Answer)
        self.assertEqual(AudienceModelAdmin.model, Audience)
        self.assertEqual(NextStepModelAdmin.model, NextStep)
        self.assertEqual(SubCategoryModelAdmin.model, SubCategory)
        self.assertEqual(AudienceModelAdmin.model, Audience)
        self.assertEqual(CategoryModelAdmin.model, Category)
