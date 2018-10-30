from django.test import TestCase

from wagtail.tests.testapp.models import SimplePage
from wagtail.wagtailcore.models import Site

from v1.blocks import ReusableTextChooserBlock
from v1.models.snippets import Contact, ReusableText


class TestUnicodeCompatibility(TestCase):
    def test_unicode_contact_heading_str(self):
        contact = Contact(heading=u'Unicod\xeb')
        self.assertEqual(str(contact), 'Unicod\xc3\xab')
        self.assertIsInstance(str(contact), str)

    def test_unicode_contact_heading_unicode(self):
        contact = Contact(heading=u'Unicod\xeb')
        self.assertEqual(unicode(contact), u'Unicod\xeb')
        self.assertIsInstance(unicode(contact), unicode)


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
