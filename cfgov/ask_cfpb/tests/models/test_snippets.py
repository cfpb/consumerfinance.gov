# -*- coding: utf-8 -*-

from django.test import TestCase

from ask_cfpb.models.snippets import GlossaryTerm
from v1.blocks import ReusableTextChooserBlock
from v1.models.snippets import ReusableText


class TestGlossaryTerm(TestCase):
    def test_term(self):
        glossary_term = GlossaryTerm(name_en='cool', name_es='chévere')
        glossary_term.save()
        self.assertEqual(glossary_term.name('es'), 'chévere')
        self.assertEqual(glossary_term.name(), 'cool')
        self.assertEqual(glossary_term.name('en'), 'cool')

    def test_answer_page_url_no_answer_page(self):
        glossary_term = GlossaryTerm(name_en='foo')
        glossary_term.save()
        self.assertIsNone(glossary_term.answer_page_url('es'))
        self.assertIsNone(glossary_term.answer_page_url())
        self.assertIsNone(glossary_term.answer_page_url('en'))

    def test_presence_of_heading(self):
        sidefoot_heading = 'Reusable text snippet heading'
        html = '<p>This is the text of the reusable snippet.</p>'
        block = ReusableTextChooserBlock(ReusableText)
        self.assertIn(
            '<h2 class="a-heading">',
            block.render({
                'sidefoot_heading': sidefoot_heading,
                'text': html
            })
        )

    def test_lack_of_heading(self):
        sidefoot_heading = None
        html = '<p>This is the text of the reusable snippet.</p>'
        block = ReusableTextChooserBlock(ReusableText)
        self.assertNotIn(
            '<h2 class="a-heading">',
            block.render({
                'sidefoot_heading': sidefoot_heading,
                'text': html
            })
        )
