# -*- coding: utf-8 -*-
from unittest import skipIf

from django.test import TestCase

from wagtail.core.models import Site
from wagtail.tests.testapp.models import SimplePage

from v1.blocks import ReusableTextChooserBlock
from v1.models.snippets import Contact, RelatedResource, ReusableText


class TestUnicodeCompatibility(TestCase):
    def test_unicode_contact_heading_unicode(self):
        contact = Contact(heading='Unicod\xeb')
        self.assertEqual(str(contact), 'Unicod\xeb')
        self.assertIsInstance(str(contact), str)


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
