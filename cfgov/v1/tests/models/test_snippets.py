# -*- coding: utf-8 -*-

import six
from unittest import skipIf

from django.test import TestCase

from wagtail.tests.testapp.models import SimplePage
from wagtail.wagtailcore.models import Site

from v1.blocks import ReusableTextChooserBlock
from v1.models.snippets import (
    Contact, GlossaryTerm, RelatedResource, ReusableText
)



class TestUnicodeCompatibility(TestCase):
    @skipIf(six.PY3, "all strings are unicode")
    def test_unicode_contact_heading_str(self):
        contact = Contact(heading=u'Unicod\xeb')
        self.assertEqual(str(contact), 'Unicod\xc3\xab')
        self.assertIsInstance(str(contact), str)

    def test_unicode_contact_heading_unicode(self):
        contact = Contact(heading=u'Unicod\xeb')
        self.assertEqual(six.text_type(contact), u'Unicod\xeb')
        self.assertIsInstance(six.text_type(contact), six.text_type)


class TestTranslations(TestCase):

    def test_related_resource_translations(self):

        test_resource = RelatedResource(
            title='English title',
            title_es='Spanish title',
            text='English text.',
            text_es='Spanish text.',
        )
        self.assertEqual(
            str(test_resource), test_resource.title)
        self.assertEqual(
            test_resource.trans_title(), test_resource.title)
        self.assertEqual(
            test_resource.trans_text(), test_resource.text)
        self.assertEqual(
            test_resource.trans_title('es'), test_resource.title_es)
        self.assertEqual(
            test_resource.trans_text('es'), test_resource.text_es)


class TestModelStrings(TestCase):

    def test_reusable_text_string(self):
        test_snippet = ReusableText(
            title='Snippet title',
            sidefoot_heading='Sidefoot heading',
            text='Snippet text')
        self.assertEqual(str(test_snippet), test_snippet.title)


class TestReusableTextRendering(TestCase):
    def test_links_get_expanded(self):
        page = SimplePage(title='foo', slug='foo', content='content')
        default_site = Site.objects.get(is_default_site=True)
        default_site.root_page.add_child(instance=page)

        html = '<a linktype="page" id="{}">Link</a>'.format(page.pk)
        block = ReusableTextChooserBlock(ReusableText)
        self.assertIn('<a href="/foo/">', block.render({'text': html}))

    def test_nonexistent_links_return_empty_link(self):
        html = '<a linktype="page" id="12345">Link</a>'
        block = ReusableTextChooserBlock(ReusableText)
        self.assertIn('<a>', block.render({'text': html}))


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
