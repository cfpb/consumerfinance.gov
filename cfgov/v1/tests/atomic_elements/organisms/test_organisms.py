from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.test import Client, RequestFactory, SimpleTestCase, TestCase

from wagtail.core.blocks import StreamValue
from wagtail.core.models import Site
from wagtail.images.tests.utils import get_test_image_file

from wagtailmedia.models import Media

from scripts import _atomic_helpers as atomic
from v1.atomic_elements.organisms import (
    AudioPlayer, FeaturedContent, InfoUnitGroup, TableBlock, VideoPlayer
)
from v1.models import (
    BrowsePage, CFGOVImage, Contact, LandingPage, LearnPage, Resource,
    SublandingPage
)
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
        self.assertContains(response, 'Ext. 1234')
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
        self.assertContains(response, 'Ext. 1234')
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

        self.assertRegex(html, 'Header One')
        self.assertRegex(html, 'Row 1-1')
        self.assertRegex(html, 'Row 2-1')

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
        self.assertContains(response, 'January&nbsp;2015')
        self.assertContains(response, 'Loans originated')
        self.assertContains(response, 'Dollar value of new loans')
        self.assertContains(response, 'In year-over-year originations')
        # Should not include inquiry or tightness information
        self.assertNotContains(response, '7.4% decrease')
        self.assertNotContains(response, 'In year-over-year inquiries')
        self.assertNotContains(response, '2.8% increase')
        self.assertNotContains(response, 'In year-over-year credit tightness')

    def test_data_snapshot_with_optional_fields(self):
        """ Data Snapshot with inquiry and tightness information correctly renders
        fields on a Browse Page"""
        browse_page = BrowsePage(
            title='Browse Page',
            slug='browse',
        )

        # Adds a AUT market to a browse page
        browse_page.content = StreamValue(
            browse_page.content.stream_block,
            [atomic.data_snapshot_with_optional_fields],
            True
        )
        publish_page(child=browse_page)

        response = self.client.get('/browse/')
        self.assertContains(response, '5 million')
        self.assertContains(response, '$64 billion')
        self.assertContains(response, '5% increase')
        self.assertContains(response, 'January&nbsp;2015')
        self.assertContains(response, 'Loans originated')
        self.assertContains(response, 'Dollar value of new loans')
        self.assertContains(response, 'In year-over-year originations')
        # Should  include inquiry or tightness information
        self.assertContains(response, '7.4% decrease')
        self.assertContains(response, 'In year-over-year inquiries')
        self.assertContains(response, '2.8% increase')
        self.assertContains(response, 'In year-over-year credit tightness')

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
        self.assertContains(response, 'Data not final.')
        self.assertContains(
            response,
            'The most recent data available in this visualization are for April 2016'
        )
        self.assertContains(response, 'January 2018')

    def test_resource_list(self):
        """ Resource List renders thumbnails when show_thumbnails is True"""
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
        self.assertContains(response, 'Test Resource List')
        self.assertContains(response, 'Test Resource')

    def test_resource_list_show_thumbnails_false(self):
        """ Resource List doesn't show thumbs when show_thumbnails is False"""
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
        self.assertNotContains(response, 'o-resource-list_list-thumbnail')

    def test_resource_list_show_thumbnails_true(self):
        """ Resource List shows thumbnails when show_thumbnails is True"""
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
        self.assertContains(response, 'o-resource-list_list-thumbnail')

    def test_resource_list_set_col_width(self):
        """ Resource List Assets column width is fixed when set"""
        assets_width_page = BrowsePage(
            title='Assets Width Test Page',
            slug='assets-width',
        )
        assets_width_page.content = StreamValue(
            assets_width_page.content.stream_block,
            [atomic.snippet_list_actions_column_width_40],
            True
        )
        publish_page(child=assets_width_page)

        self.create_resource()

        response = self.client.get('/assets-width/')
        self.assertContains(response, 'u-w40pct"')


class FeaturedContentTests(TestCase):
    def setUp(self):
        self.page = Site.objects.get(is_default_site=True).root_page
        self.image = CFGOVImage.objects.create(
            title='test',
            file=get_test_image_file()
        )

    def test_value_contains_single_list_of_links(self):
        block = FeaturedContent()
        value = block.to_python({
            'post': self.page.pk,
            'show_post_link': True,
            'post_link_text': 'This is a post',
            'links': [
                {'text': 'A link', 'url': '/foo/'},
                {'text': 'Another link', 'url': '/bar/'},
            ],
        })

        self.assertEqual(value.links, [
            {'url': self.page.url, 'text': 'This is a post'},
            {'url': '/foo/', 'text': 'A link', 'aria_label': None},
            {'url': '/bar/', 'text': 'Another link', 'aria_label': None},
        ])

    def test_render(self):
        block = FeaturedContent()
        value = block.to_python({
            'heading': 'Featured content',
            'body': 'This is the body',
            'post': self.page.pk,
            'show_post_link': True,
            'post_link_text': 'This is a post',
            'links': [
                {'text': 'A link', 'url': '/foo/'},
                {'text': 'Another link', 'url': '/bar/'},
            ],
            'video': {
                'video_id': '1V0Ax9OIc84',
		'thumbnail_image': self.image.pk,
            },
        })

        request = RequestFactory().get('/')
        html = block.render(value, context={'request': request})

        # All links get rendered properly.
        for url, text in (
            (self.page.url, 'This is a post'),
            ('/foo/', 'A link'),
            ('/bar/', 'Another link'),
        ):
            self.assertIn(
                f'<a class="m-list_link"\n                       '
                f'href="{url}"\n                       >{text}</a>',
                html
            )

        # VideoPlayer renders with is_fcm=True and the proper thumbnail.
        self.assertNotIn('o-video-player_video-container__flexible', html)
        self.assertRegex(
            html,
            r'src="/f/images/test.*\.original\.png"'
        )


class TestInfoUnitGroup(TestCase):
    def setUp(self):
        self.block = InfoUnitGroup()
        self.image = CFGOVImage.objects.create(
            title='test',
            file=get_test_image_file()
        )

    def test_no_heading_or_intro_ok(self):
        value = self.block.to_python({})
        try:
            self.block.clean(value)
        except ValidationError:  # pragma: nocover
            self.fail('no heading and no intro should not fail validation')

    def test_heading_only_ok(self):
        value = self.block.to_python({
            'heading': {
                'text': 'Heading'
            }
        })
        try:
            self.block.clean(value)
        except ValidationError:  # pragma: nocover
            self.fail('heading alone should not fail validation')

    def test_heading_and_intro_ok(self):
        value = self.block.to_python({
            'heading': {
                'text': 'Heading'
            },
            'intro': '<p>Rich txt</p>'
        })
        try:
            self.block.clean(value)
        except ValidationError:  # pragma: nocover
            self.fail('heading with intro should not fail validation')

    def test_2575_with_image_ok(self):
        value = self.block.to_python({
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
            self.block.clean(value)
        except ValidationError:  # pragma: nocover
            self.fail('25-75 group with info unit that has an image validates')

    def test_2575_with_no_images_fails_validation(self):
        value = self.block.to_python({
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
            self.block.clean(value)

    def test_2575_with_some_images_fails(self):
        value = self.block.to_python({
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
            self.block.clean(value)


class VideoPlayerTests(SimpleTestCase):
    def test_video_id_required_by_default(self):
        block = VideoPlayer()
        value = block.to_python({'video_id': None})

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_video_id_not_required_if_block_is_not_required(self):
        block = VideoPlayer(required=False)
        value = block.to_python({'video_id': None})

        try:
            block.clean(value)
        except ValidationError as e:  # pragma: nocover
            self.fail('Optional VideoPlayers should not require sub-fields')

    def test_invalid_video_id(self):
        block = VideoPlayer()
        value = block.to_python({'video_url': 'Invalid YouTube ID'})

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_valid_video_id(self):
        block = VideoPlayer(required=False)
        value = block.to_python({'video_id': '1V0Ax9OIc84'})

        try:
            block.clean(value)
        except ValidationError as e:  # pragma: nocover
            self.fail('VideoPlayer should support valid YouTube IDs')

    def test_render(self):
        block = VideoPlayer()
        value = block.to_python({'video_id': '1V0Ax9OIc84'})

        request = RequestFactory().get('/')
        html = block.render(value, context={'request': request})

        self.assertIn(
            'href="https://www.youtube.com/embed/1V0Ax9OIc84',
            html
        )

        # Default no-JS image is used if no thumbnail is provided.
        self.assertIn(
            'src="/static/img/cfpb_video_cover_card_954x200.png"',
            html
        )

        # Default behavior doesn't render as FCM.
        self.assertNotIn('o-featured-content-module_visual', html)


class VideoPlayerThumbnailTests(TestCase):
    def setUp(self):
        self.image = CFGOVImage.objects.create(
            title='test',
            file=get_test_image_file()
        )

    def test_thumbnail_image_without_video_id_fails_validation(self):
        block = VideoPlayer(required=False)
        value = block.to_python({'thumbnail_image': self.image.pk})

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_value_contains_thumbnail_url(self):
        block = VideoPlayer()
        value = block.to_python({
            'video_id': '1V0Ax9OIc84',
            'thumbnail_image': self.image.pk,
        })

        self.assertRegex(
            value.thumbnail_url,
            r'^.*/images/test.*\.original\.png$'
        )

    def test_render(self):
        block = VideoPlayer()
        value = block.to_python({
            'video_id': '1V0Ax9OIc84',
            'thumbnail_image': self.image.pk,
        })

        request = RequestFactory().get('/')
        html = block.render(value, context={'request': request})

        self.assertIn(
            'href="https://www.youtube.com/embed/1V0Ax9OIc84',
            html
        )
        self.assertRegex(
            html,
            r'src="/f/images/test.*\.original\.png"'
        )


class TestAudioPlayer(TestCase):
    def test_render_audio_player(self):
        block = AudioPlayer()
        fake_file = ContentFile('A boring example mp3')
        fake_file.name = 'test.mp3'
        media = Media.objects.create(
            title='Test audio file',
            type='audio',
            duration=100,
            file=File(fake_file)
        )
        value = block.to_python({
            'audio_file': media.pk,
        })

        html = block.render(value)

        self.assertInHTML(
            (
                '<audio class="o-audio-player" controls preload="metadata"'
                '       data-title="Test audio file">'
                '    <source src="/f/media/test.mp3" type="audio/mpeg">'
                '    Your browser does not support this audio player.'
                '</audio>'
            ),
            html
        )

    def test_audio_player_with_video_file_returns_error(self):
        block = AudioPlayer()
        fake_file = ContentFile('Example video')
        fake_file.name = 'test.mp4'
        media = Media.objects.create(
            title='Test video file',
            type='video',
            duration=100,
            file=File(fake_file)
        )
        value = block.to_python({
            'audio_file': media.pk,
        })

        html = block.render(value)
        self.assertInHTML(
            '<b>Warning:</b>',
            html
        )
