from django.test import TestCase

from wagtail.tests.testapp.models import SimplePage
from wagtail.wagtailcore.models import Site

from v1.blocks import ReusableTextChooserBlock
from v1.models.snippets import Contact, Resource, ReusableText


class TestFilterByTags(TestCase):
    def setUp(self):
        self.snippet1 = Resource.objects.create(title='Test snippet 1')
        self.snippet1.tags.add('tagA')
        self.snippet2 = Resource.objects.create(title='Test snippet 2')
        self.snippet2.tags.add('tagA')
        self.snippet2.tags.add('tagB')

    def test_empty_list_argument_returns_all(self):
        self.assertSequenceEqual(
            Resource.objects.filter_by_tags([]),
            [self.snippet1, self.snippet2]
        )

    def test_all_items_with_single_tag_are_returned(self):
        self.assertSequenceEqual(
            Resource.objects.filter_by_tags(['tagA']),
            [self.snippet1, self.snippet2]
        )

    def test_nothing_returned_when_tag_is_unused(self):
        self.assertSequenceEqual(
            Resource.objects.filter_by_tags(['tagC']),
            []
        )

    def test_item_with_multiple_tags_is_returned(self):
        self.assertIn(
            self.snippet2,
            Resource.objects.filter_by_tags(['tagA', 'tagB'])
        )

    def test_item_with_only_some_of_selected_tags_is_not_returned(self):
        self.assertNotIn(
            self.snippet1,
            Resource.objects.filter_by_tags(['tagA', 'tagB'])
        )


class TestOrderedResources(TestCase):
    def setUp(self):
        self.snippetBBC = Resource.objects.create(title='BBC')
        self.snippetZebra = Resource.objects.create(title='Zebra')
        self.snippetAbc = Resource.objects.create(title='Abc')

    def test_default_alphabetical_ordering(self):
        self.assertSequenceEqual(
            Resource.objects.all(),
            [self.snippetAbc, self.snippetBBC, self.snippetZebra]
        )

    def test_total_explicit_ordering(self):
        self.snippetAbc.order = 23
        self.snippetAbc.save()
        self.snippetBBC.order = 1
        self.snippetBBC.save()
        self.snippetZebra.order = 32000
        self.snippetZebra.save()

        self.assertSequenceEqual(
            Resource.objects.all(),
            [self.snippetBBC, self.snippetAbc, self.snippetZebra]
        )

class TestUnicodeCompatibility(TestCase):
    def test_unicode_contact_heading_str(self):
        contact = Contact(heading=u'Unicod\xeb')
        self.assertEqual(str(contact), 'Unicod\xc3\xab')
        self.assertIsInstance(str(contact), str)

    def test_unicode_contact_heading_unicode(self):
        contact = Contact(heading=u'Unicod\xeb')
        self.assertEqual(unicode(contact), u'Unicod\xeb')
        self.assertIsInstance(unicode(contact), unicode)

    def test_unicode_resource_title_str(self):
        resource = Resource(title=u'Unicod\xeb')
        self.assertEqual(str(resource), 'Unicod\xc3\xab')
        self.assertIsInstance(str(resource), str)

    def test_unicode_resource_title_unicode(self):
        resource = Resource(title=u'Unicod\xeb')
        self.assertEqual(unicode(resource), u'Unicod\xeb')
        self.assertIsInstance(unicode(resource), unicode)


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
