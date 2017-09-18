from scripts import _atomic_helpers as atomic

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from wagtail.wagtailcore.blocks import StreamValue
from wagtail.wagtailimages.tests.utils import get_test_image_file

from v1.atomic_elements.organisms import InfoUnitGroup, TableBlock
from v1.models.browse_page import BrowsePage
from v1.models.images import CFGOVImage
from v1.models.landing_page import LandingPage
from v1.models.learn_page import LearnPage
from v1.models.snippets import Contact, Resource
from v1.models.sublanding_page import SublandingPage
from v1.tests.wagtail_pages.helpers import publish_page

django_client = Client()

'''
TODO: Create tests for the following organisms:
          - FilterableListControls
          - Sidebar Breakout
          - PostPreviewSnapshot
          - RelatedPosts
'''


class OrganismsTestCase(TestCase):
    def get_contact(self):
        contact = Contact(heading='Test User')
        contact.heading = 'this is a heading'
        contact.body = 'this is a body'
        contact.contact_info = StreamValue(
            contact.contact_info.stream_block,
            [
                atomic.contact_email,
                atomic.contact_phone,
                atomic.contact_address
            ],
            True
        )
        contact.save()
        return contact

    def create_resource(self):
        thumb = CFGOVImage.objects.create(
            title='test resource thumbnail',
            file=get_test_image_file()
        )

        resource = Resource(title='Test Resource')
        resource.thumbnail = thumb
        resource.save()

    def test_well(self):
        """Well content correctly displays on a Landing Page"""
        landing_page = LandingPage(
                title='Landing Page',
                slug='landing',
        )
        landing_page.content = StreamValue(
            landing_page.content.stream_block,
            [atomic.well],
            True
        )
        publish_page(child=landing_page)
        response = django_client.get('/landing/')
        self.assertContains(response, 'this is well content')

    def test_main_contact_info(self):
        """Main contact info correctly displays on a Sublanding Page"""
        sublanding_page = SublandingPage(
                title='Sublanding Page',
                slug='sublanding',
        )
        contact = self.get_contact()
        sublanding_page.content = StreamValue(
            sublanding_page.content.stream_block,
            [atomic.main_contact_info(contact.id)],
            True
        )
        publish_page(child=sublanding_page)
        response = django_client.get('/sublanding/')
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, '(515) 123-4567')
        self.assertContains(response, '123 abc street')
        self.assertContains(response, 'this is a heading')
        self.assertContains(response, 'this is a body')
        self.assertNotContains(response, 'Contact Information') # Only shown on sidebar

    def test_sidebar_contact_info(self):
        """Sidebar contact info correctly displays on a Landing Page"""
        landing_page = LandingPage(
                title='Landing Page',
                slug='landing',
        )
        contact = self.get_contact()
        landing_page.sidefoot = StreamValue(
            landing_page.sidefoot.stream_block,
            [atomic.sidebar_contact(contact.id)],
            True
        )
        publish_page(child=landing_page)
        response = django_client.get('/landing/')
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, '(515) 123-4567')
        self.assertContains(response, '123 abc street')
        self.assertContains(response, 'this is a heading')
        self.assertContains(response, 'this is a body')
        self.assertContains(response, 'Contact Information') # This is specific to sidebar

    def test_full_width_text(self):
        """Full width text content correctly displays on a Learn Page"""
        learn_page = LearnPage(
                title='Learn Page',
                slug='learn',
        )
        learn_page.content = StreamValue(
            learn_page.content.stream_block,
            [atomic.full_width_text],
            True
        )
        publish_page(child=learn_page)
        response = django_client.get('/learn/')
        self.assertContains(response, 'Full width text content')

    def test_image_text_groups(self):
        """Image Text Groups correctly display on a Landing Page"""
        landing_page = LandingPage(
            title='Landing Page',
            slug='landing',
        )
        landing_page.content = StreamValue(
            landing_page.content.stream_block,
            [
                atomic.image_text_50_50_group,
                atomic.image_text_25_75_group
            ],
            True,
        )
        publish_page(child=landing_page)
        response = django_client.get('/landing/')
        self.assertContains(response, 'Image 25 75 Group')
        self.assertContains(response, 'Image 50 50 Group')

    def test_half_width_link_blob_group(self):
        """Half width link blob group correctly displays on a Landing Page"""
        landing_page = LandingPage(
            title='Landing Page',
            slug='landing',
        )
        landing_page.content = StreamValue(
            landing_page.content.stream_block,
            [atomic.half_width_link_blob_group],
            True
        )
        publish_page(child=landing_page)
        response = django_client.get('/landing/')
        self.assertContains(response, 'Half Width Link Blob Group')

    def test_info_unit_group(self):
        """Info Unit Group correctly displays on a Landing Page"""
        landing_page = LandingPage(
            title='Landing Page',
            slug='landing',
        )
        landing_page.content = StreamValue(
            landing_page.content.stream_block,
            [atomic.info_unit_group],
            True
        )
        publish_page(child=landing_page)
        response = django_client.get('/landing/')
        self.assertContains(response, 'Info Unit Group')

    # TODO: More comprehensive test for this organism
    def test_reg_comment(self):
        """RegComment correctly displays on a Sublanding Page"""
        sublanding_page = SublandingPage(
            title='Sublanding Page',
            slug='sublanding',
        )
        sublanding_page.content = StreamValue(
            sublanding_page.content.stream_block,
            [atomic.reg_comment],
            True
        )
        publish_page(child=sublanding_page)
        response = django_client.get('/sublanding/')
        self.assertContains(response, 'Enter your comments')

    def test_tableblock(self):
        """Table correctly displays on a Learn Page"""
        learn_page = LearnPage(
                title='Learn Page',
                slug='learn',
        )
        learn_page.content = StreamValue(
            learn_page.content.stream_block,
            [atomic.table_block],
            True
        )
        publish_page(child=learn_page)
        response = django_client.get('/learn/')
        self.assertContains(response, 'Header One')
        self.assertContains(response, 'Row 1-1')
        self.assertContains(response, 'Row 2-1')

    def test_tableblock_missing_attributes(self):
        """Table correctly displays when value dictionary is missing attributes"""
        table_context = dict(atomic.table_block)
        value = table_context.get('value')
        del value['first_row_is_table_header']
        del value['first_col_is_header']
        table = TableBlock()
        html = str(table.render(table.to_python(value)))

        self.assertRegexpMatches(html, 'Header One')
        self.assertRegexpMatches(html, 'Row 1-1')
        self.assertRegexpMatches(html, 'Row 2-1')

        self.assertIsNone(value.get('first_row_is_table_header'), None)
        self.assertIsNone(value.get('first_col_is_header'), None)

        with self.assertRaises(KeyError):
            value['first_row_is_table_header']
        with self.assertRaises(KeyError):
            value['first_col_is_header']

    def test_expandable_group(self):
        """Expandable group correctly displays on a Browse Page"""
        browse_page = BrowsePage(
            title='Browse Page',
            slug='browse',
        )
        browse_page.content = StreamValue(
            browse_page.content.stream_block,
            [atomic.expandable_group],
            True
        )
        publish_page(child=browse_page)
        response = django_client.get('/browse/')
        self.assertContains(response, 'Expandable Group')
        self.assertContains(response, 'Expandable group body')

    def test_item_introduction(self):
        """Item introduction correctly displays on a Learn Page"""
        learn_page = LearnPage(
                title='Learn Page',
                slug='learn',
        )
        learn_page.header = StreamValue(
            learn_page.header.stream_block,
            [atomic.item_introduction],
            True
        )
        publish_page(child=learn_page)
        response = django_client.get('/learn/')
        self.assertContains(response, 'Item Introduction')
        self.assertContains(response, 'Item introduction body')

    def test_html_block(self):
        """ HTML Block correctly renders HTML on a Browse Page"""
        browse_page = BrowsePage(
            title='Browse Page',
            slug='browse',
        )
        browse_page.content = StreamValue(
            browse_page.content.stream_block,
            [atomic.html_block],
            True
        )
        publish_page(child=browse_page)
        response = self.client.get('/browse/')
        self.assertContains(response, 'Age 30 to 44')

    def test_data_snapshot(self):
        """ Data Snapshot correctly renders fields on a Browse Page"""
        browse_page = BrowsePage(
            title='Browse Page',
            slug='browse',
        )

        # Adds a AUT market to a browse page
        browse_page.content = StreamValue(
            browse_page.content.stream_block,
            [atomic.data_snapshot],
            True
        )
        publish_page(child=browse_page)

        response = self.client.get('/browse/')
        self.assertContains(response, '5 million')
        self.assertContains(response, '$64 billion')
        self.assertContains(response, '5% increase')
        self.assertContains(response, 'January 2015')
        self.assertContains(response, 'Auto loans originated')
        self.assertContains(response, 'Dollar value of new loans')
        self.assertContains(response, 'In year-over-year originations')

    def test_chart_block(self):
        """ Chart Block correctly renders fields on a Browse Page"""
        browse_page = BrowsePage(
            title='Browse Page',
            slug='browse',
        )

        # Adds a AUT market to a browse page
        browse_page.content = StreamValue(
            browse_page.content.stream_block,
            [atomic.chart_block],
            True
        )
        publish_page(child=browse_page)

        response = self.client.get('/browse/')
        self.assertContains(response, 'Volume of credit cards originated')
        self.assertContains(response, 'foo/bar.csv')
        self.assertContains(response, 'Data not final')
        self.assertContains(
            response,
            'The most recent data available in each visualization is for April 2016'
        )
        self.assertContains(response, 'January 2018')

    def test_snippet_list(self):
        """ Snippet List renders thumbnails when show_thumbnails is True"""
        browse_page = BrowsePage(
            title='Browse Page',
            slug='browse',
        )
        browse_page.content = StreamValue(
            browse_page.content.stream_block,
            [atomic.snippet_list_show_thumbnails_false],
            True
        )
        publish_page(child=browse_page)

        self.create_resource()

        response = self.client.get('/browse/')
        self.assertContains(response, 'Test Snippet List')
        self.assertContains(response, 'Test Resource')

    def test_snippet_list_show_thumbnails_false(self):
        """ Snippet List doesn't show thumbs when show_thumbnails is False"""
        no_thumbnails_page = BrowsePage(
            title='No Thumbnails Page',
            slug='no-thumbnails',
        )
        no_thumbnails_page.content = StreamValue(
            no_thumbnails_page.content.stream_block,
            [atomic.snippet_list_show_thumbnails_false],
            True
        )
        publish_page(child=no_thumbnails_page)

        self.create_resource()

        response = self.client.get('/no-thumbnails/')
        self.assertNotContains(response, 'o-snippet-list_list-thumbnail')

    def test_snippet_list_show_thumbnails_true(self):
        """ Snippet List shows thumbnails when show_thumbnails is True"""
        thumbnails_page = BrowsePage(
            title='Thumbnails Page',
            slug='thumbnails',
        )
        thumbnails_page.content = StreamValue(
            thumbnails_page.content.stream_block,
            [atomic.snippet_list_show_thumbnails_true],
            True
        )
        publish_page(child=thumbnails_page)

        self.create_resource()

        response = self.client.get('/thumbnails/')
        self.assertContains(response, 'o-snippet-list_list-thumbnail')


class TestInfoUnitGroup(TestCase):
    def setUp(self):
        self.image = CFGOVImage.objects.create(
            title='test',
            file=get_test_image_file()
        )

    def test_no_heading_or_intro_ok(self):
        block = InfoUnitGroup()
        value = block.to_python({})

        try:
            block.clean(value)
        except ValidationError:
            self.fail('no heading and no intro should not fail validation')

    def test_heading_only_ok(self):
        block = InfoUnitGroup()
        value = block.to_python({
            'heading': {
                'text': 'Heading'
            }
        })

        try:
            block.clean(value)
        except ValidationError:
            self.fail('heading alone should not fail validation')

    def test_intro_only_fails_validation(self):
        block = InfoUnitGroup()
        value = block.to_python({'intro': '<p>Only an intro</p>'})

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_heading_and_intro_ok(self):
        block = InfoUnitGroup()
        value = block.to_python({
            'heading': {
                'text': 'Heading'
            },
            'intro': '<p>Rich txt</p>'
        })

        try:
            block.clean(value)
        except ValidationError:
            self.fail('heading with intro should not fail validation')

    def test_2575_with_image_ok(self):
        block = InfoUnitGroup()
        value = block.to_python({
            'format': '25-75',
            'info_units': [
                {
                    'image': {
                        'upload': self.image.pk
                    },
                    'links': [],  # must remove default empty link
                }
            ]
        })

        try:
            block.clean(value)
        except ValidationError:
            self.fail('25-75 group with info unit that has an image validates')

    def test_2575_with_no_images_fails_validation(self):
        block = InfoUnitGroup()
        value = block.to_python({
            'format': '25-75',
            'info_units': [
                {
                    'image': {},
                    'body': '<p>Info unit with no image</p>',
                    'links': [],  # must remove default empty link
                }
            ]
        })

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_2575_with_some_images_fails(self):
        block = InfoUnitGroup()
        value = block.to_python({
            'format': '25-75',
            'info_units': [
                {
                    'image': {
                        'upload': self.image.pk
                    },
                    'links': [],  # must remove default empty link
                },
                {
                    'image': {},
                    'body': '<p>Info unit with no image</p>',
                    'links': [],  # must remove default empty link
                }
            ]
        })

        with self.assertRaises(ValidationError):
            block.clean(value)
