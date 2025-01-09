from datetime import date

from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.test import Client, RequestFactory, SimpleTestCase, TestCase

from wagtail.blocks import StreamValue
from wagtail.images.tests.utils import get_test_image_file
from wagtail.models import Site

from wagtailmedia.models import Media

from core.templatetags.svg_icon import svg_icon
from core.testutils.test_cases import WagtailPageTreeTestCase
from scripts import _atomic_helpers as atomic
from v1.atomic_elements.organisms import (
    AudioPlayer,
    FeaturedContent,
    InfoUnitGroup,
    ItemIntroduction,
    VideoPlayer,
)
from v1.models import (
    BrowseFilterablePage,
    BrowsePage,
    CFGOVImage,
    CFGOVPageCategory,
    Contact,
    LandingPage,
    LearnPage,
    SublandingPage,
)
from v1.tests.wagtail_pages.helpers import publish_page


django_client = Client()

"""
TODO: Create tests for the following organisms:
          - FilterableListControls
          - Sidebar Breakout
          - PostPreviewSnapshot
          - RelatedPosts
"""


class OrganismsTestCase(TestCase):
    def get_contact(self):
        contact = Contact(heading="Test User")
        contact.heading = "this is a heading"
        contact.body = "this is a body"
        contact.contact_info = StreamValue(
            contact.contact_info.stream_block,
            [
                atomic.contact_email,
                atomic.contact_phone,
                atomic.contact_address,
            ],
            True,
        )
        contact.save()
        return contact

    def test_well(self):
        """Well content correctly displays on a Landing Page"""
        landing_page = LandingPage(title="Landing Page", slug="landing")
        landing_page.content = StreamValue(
            landing_page.content.stream_block, [atomic.well], True
        )
        publish_page(child=landing_page)
        response = django_client.get("/landing/")
        self.assertContains(response, "this is well content")

    def test_main_contact_info(self):
        """Main contact info correctly displays on a Sublanding Page"""
        sublanding_page = SublandingPage(
            title="Sublanding Page",
            slug="sublanding",
        )
        contact = self.get_contact()
        sublanding_page.content = StreamValue(
            sublanding_page.content.stream_block,
            [atomic.main_contact_info(contact.id)],
            True,
        )
        publish_page(child=sublanding_page)
        response = django_client.get("/sublanding/")
        self.assertContains(response, "test@example.com")
        self.assertContains(response, "(515) 123-4567")
        self.assertContains(response, "Ext. 1234")
        self.assertContains(response, "123 abc street")
        self.assertContains(response, "this is a heading")
        self.assertContains(response, "this is a body")
        # Only shown on sidebar
        self.assertNotContains(response, "Contact Information")

    def test_sidebar_contact_info(self):
        """Sidebar contact info correctly displays on a Landing Page"""
        landing_page = LandingPage(title="Landing Page", slug="landing")
        contact = self.get_contact()
        landing_page.sidefoot = StreamValue(
            landing_page.sidefoot.stream_block,
            [atomic.sidebar_contact(contact.id)],
            True,
        )
        publish_page(child=landing_page)
        response = django_client.get("/landing/")
        self.assertContains(response, "test@example.com")
        self.assertContains(response, "(515) 123-4567")
        self.assertContains(response, "Ext. 1234")
        self.assertContains(response, "123 abc street")
        self.assertContains(response, "this is a heading")
        self.assertContains(response, "this is a body")
        # This is specific to sidebar
        self.assertContains(response, "Contact Information")

    def test_full_width_text(self):
        """Full width text content correctly displays on a Learn Page"""
        learn_page = LearnPage(title="Learn Page", slug="learn")
        learn_page.content = StreamValue(
            learn_page.content.stream_block, [atomic.full_width_text], True
        )
        publish_page(child=learn_page)
        response = django_client.get("/learn/")
        self.assertContains(response, "Full width text content")

    def test_info_unit_group(self):
        """Info Unit Group correctly displays on a Landing Page"""
        landing_page = LandingPage(
            title="Landing Page",
            slug="landing",
        )
        landing_page.content = StreamValue(
            landing_page.content.stream_block, [atomic.info_unit_group], True
        )
        publish_page(child=landing_page)
        response = django_client.get("/landing/")
        self.assertContains(response, "Info Unit Group")

    def test_expandable_group(self):
        """Expandable group correctly displays on a Browse Page"""
        browse_page = BrowsePage(
            title="Browse Page",
            slug="browse",
        )
        browse_page.content = StreamValue(
            browse_page.content.stream_block, [atomic.expandable_group], True
        )
        publish_page(child=browse_page)
        response = django_client.get("/browse/")
        self.assertContains(response, "Expandable Group")
        self.assertContains(response, "Expandable group body")

    def test_item_introduction(self):
        """Item introduction correctly displays on a Learn Page"""
        learn_page = LearnPage(title="Learn Page", slug="learn")
        learn_page.header = StreamValue(
            learn_page.header.stream_block, [atomic.item_introduction], True
        )
        publish_page(child=learn_page)
        response = django_client.get("/learn/")
        self.assertContains(response, "Item Introduction")
        self.assertContains(response, "Item introduction body")

    def test_data_snapshot(self):
        """Data Snapshot correctly renders fields on a Browse Page"""
        browse_page = BrowsePage(
            title="Browse Page",
            slug="browse",
        )

        # Adds a AUT market to a browse page
        browse_page.content = StreamValue(
            browse_page.content.stream_block, [atomic.data_snapshot], True
        )
        publish_page(child=browse_page)

        response = self.client.get("/browse/")
        self.assertContains(response, "5 million")
        self.assertContains(response, "$64 billion")
        self.assertContains(response, "5% increase")
        self.assertContains(response, "January&nbsp;2015")
        self.assertContains(response, "Loans originated")
        self.assertContains(response, "Dollar value of new loans")
        self.assertContains(response, "In year-over-year originations")
        # Should not include inquiry or tightness information
        self.assertNotContains(response, "7.4% decrease")
        self.assertNotContains(response, "In year-over-year inquiries")
        self.assertNotContains(response, "2.8% increase")
        self.assertNotContains(response, "In year-over-year credit tightness")

    def test_data_snapshot_with_optional_fields(self):
        """Test rendering of Data Snapshot with inquiry and tightness data"""
        browse_page = BrowsePage(
            title="Browse Page",
            slug="browse",
        )

        # Adds a AUT market to a browse page
        browse_page.content = StreamValue(
            browse_page.content.stream_block,
            [atomic.data_snapshot_with_optional_fields],
            True,
        )
        publish_page(child=browse_page)

        response = self.client.get("/browse/")
        self.assertContains(response, "5 million")
        self.assertContains(response, "$64 billion")
        self.assertContains(response, "5% increase")
        self.assertContains(response, "January&nbsp;2015")
        self.assertContains(response, "Loans originated")
        self.assertContains(response, "Dollar value of new loans")
        self.assertContains(response, "In year-over-year originations")
        # Should  include inquiry or tightness information
        self.assertContains(response, "7.4% decrease")
        self.assertContains(response, "In year-over-year inquiries")
        self.assertContains(response, "2.8% increase")
        self.assertContains(response, "In year-over-year credit tightness")

    def test_chart_block(self):
        """Chart Block correctly renders fields on a Browse Page"""
        browse_page = BrowsePage(
            title="Browse Page",
            slug="browse",
        )

        # Adds a AUT market to a browse page
        browse_page.content = StreamValue(
            browse_page.content.stream_block, [atomic.chart_block], True
        )
        publish_page(child=browse_page)

        response = self.client.get("/browse/")
        self.assertContains(response, "Volume of credit cards originated")
        self.assertContains(response, "foo/bar.csv")
        self.assertContains(response, "Data not final.")
        self.assertContains(
            response,
            (
                "The most recent data available in this visualization are for "
                "April 2016"
            ),
        )
        self.assertContains(response, "January 2018")


class FeaturedContentTests(TestCase):
    def setUp(self):
        self.page = Site.objects.get(is_default_site=True).root_page
        self.image = CFGOVImage.objects.create(
            title="test", file=get_test_image_file()
        )

    def test_value_contains_single_list_of_links(self):
        block = FeaturedContent()
        value = block.to_python(
            {
                "post": self.page.pk,
                "show_post_link": True,
                "post_link_text": "This is a post",
                "links": [
                    {"text": "A link", "url": "/foo/"},
                    {"text": "Another link", "url": "/bar/"},
                ],
            }
        )

        self.assertEqual(
            value.links,
            [
                {"url": self.page.url, "text": "This is a post"},
                {"url": "/foo/", "text": "A link", "aria_label": None},
                {"url": "/bar/", "text": "Another link", "aria_label": None},
            ],
        )

    def test_render(self):
        block = FeaturedContent()
        value = block.to_python(
            {
                "heading": "Featured content",
                "body": "This is the body",
                "post": self.page.pk,
                "show_post_link": True,
                "post_link_text": "This is a post",
                "links": [
                    {"text": "A link", "url": "/foo/"},
                    {"text": "Another link", "url": "/bar/"},
                ],
                "video": {
                    "video_id": "1V0Ax9OIc84",
                    "thumbnail_image": self.image.pk,
                },
            }
        )

        request = RequestFactory().get("/")
        html = block.render(value, context={"request": request})

        # All links get rendered properly.
        for url, text in (
            (self.page.url, "This is a post"),
            ("/foo/", "A link"),
            ("/bar/", "Another link"),
        ):
            self.assertIn(
                f'<a class="a-link a-link--jump"\n                       href='
                f'"{url}"\n                       >\n                       \n'
                f'                       <span class="a-link__text">'
                f"{text}</span>\n                       \n"
                f"                    </a>",
                html,
            )

        # VideoPlayer renders with is_fcm=True and the proper thumbnail.
        self.assertNotIn("o-video-player_video-container__flexible", html)
        self.assertRegex(html, r'src="/f/images/test.*\.original\.png"')


class TestInfoUnitGroup(TestCase):
    def setUp(self):
        self.block = InfoUnitGroup()
        self.image = CFGOVImage.objects.create(
            title="test", file=get_test_image_file()
        )

    def test_no_heading_or_intro_ok(self):
        value = self.block.to_python({})
        try:
            self.block.clean(value)
        except ValidationError:  # pragma: nocover
            self.fail("no heading and no intro should not fail validation")

    def test_heading_only_ok(self):
        value = self.block.to_python({"heading": {"text": "Heading"}})
        try:
            self.block.clean(value)
        except ValidationError:  # pragma: nocover
            self.fail("heading alone should not fail validation")

    def test_heading_and_intro_ok(self):
        value = self.block.to_python(
            {"heading": {"text": "Heading"}, "intro": "<p>Rich txt</p>"}
        )
        try:
            self.block.clean(value)
        except ValidationError:  # pragma: nocover
            self.fail("heading with intro should not fail validation")

    def test_2575_with_image_ok(self):
        value = self.block.to_python(
            {
                "format": "25-75",
                "info_units": [
                    {
                        "image": {"upload": self.image.pk},
                        "links": [],  # must remove default empty link
                    }
                ],
            }
        )

        try:
            self.block.clean(value)
        except ValidationError:  # pragma: nocover
            self.fail("25-75 group with info unit that has an image validates")

    def test_2575_with_no_images_fails_validation(self):
        value = self.block.to_python(
            {
                "format": "25-75",
                "info_units": [
                    {
                        "image": {},
                        "body": "<p>Info unit with no image</p>",
                        "links": [],  # must remove default empty link
                    }
                ],
            }
        )

        with self.assertRaises(ValidationError):
            self.block.clean(value)

    def test_2575_with_some_images_fails(self):
        value = self.block.to_python(
            {
                "format": "25-75",
                "info_units": [
                    {
                        "image": {"upload": self.image.pk},
                        "links": [],  # must remove default empty link
                    },
                    {
                        "image": {},
                        "body": "<p>Info unit with no image</p>",
                        "links": [],  # must remove default empty link
                    },
                ],
            }
        )

        with self.assertRaises(ValidationError):
            self.block.clean(value)


class ItemIntroductionTests(WagtailPageTreeTestCase):
    @classmethod
    def get_page_tree(cls):
        return [
            (
                BrowseFilterablePage(title="landing"),
                [LearnPage(title="intro")],
            )
        ]

    def test_render(self):
        # Related objects need to be added after page tree creation.
        self.page_tree[1].authors.add("CFPB")
        self.page_tree[1].categories.add(CFGOVPageCategory(name="at-the-cfpb"))

        block = ItemIntroduction()
        value = block.to_python(
            {
                "heading": "An item introduction",
                "date": date(2024, 1, 1),
                "show_category": True,
            }
        )

        html = block.render(
            value,
            context={
                "page": self.page_tree[1],
                "request": RequestFactory().get("/intro/"),
            },
        )

        self.assertHTMLEqual(
            html,
            f"""
<div class="o-item-introduction">
    <div class="o-item-introduction__intro">
        <a class="h4" href="/landing/?categories=at-the-cfpb">
            {svg_icon("bullhorn")}
            <span class="u-visually-hidden">
                Category:
            </span>
            At the CFPB
        </a>
    </div>
    <h1>An item introduction</h1>
    <div class="meta">
        <span class="byline">By CFPB</span>
        &ndash;
        <span class="a-date">
            <span class="datetime">
                <time datetime="2024-01-01T00:00:00">JAN 01, 2024</time>
            </span>
        </span>
    </div>
</div>
""",
        )


class VideoPlayerTests(SimpleTestCase):
    def test_video_id_required_by_default(self):
        block = VideoPlayer()
        value = block.to_python({"video_id": None})

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_video_id_not_required_if_block_is_not_required(self):
        block = VideoPlayer(required=False)
        value = block.to_python({"video_id": None})

        try:
            block.clean(value)
        except ValidationError:  # pragma: nocover
            self.fail("Optional VideoPlayers should not require sub-fields")

    def test_invalid_video_id(self):
        block = VideoPlayer()
        value = block.to_python({"video_url": "Invalid YouTube ID"})

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_valid_video_id(self):
        block = VideoPlayer(required=False)
        value = block.to_python({"video_id": "1V0Ax9OIc84"})

        try:
            block.clean(value)
        except ValidationError:  # pragma: nocover
            self.fail("VideoPlayer should support valid YouTube IDs")

    def test_render(self):
        block = VideoPlayer()
        value = block.to_python({"video_id": "1V0Ax9OIc84"})

        request = RequestFactory().get("/")
        html = block.render(value, context={"request": request})

        self.assertIn('href="https://www.youtube.com/embed/1V0Ax9OIc84', html)

        # Default no-JS image is used if no thumbnail is provided.
        self.assertIn(
            'src="/static/img/cfpb_video_cover_card_954x200.png"', html
        )

        # Default behavior doesn't render as FCM.
        self.assertNotIn("o-featured-content-module_visual", html)


class VideoPlayerThumbnailTests(TestCase):
    def setUp(self):
        self.image = CFGOVImage.objects.create(
            title="test", file=get_test_image_file()
        )

    def test_thumbnail_image_without_video_id_fails_validation(self):
        block = VideoPlayer(required=False)
        value = block.to_python({"thumbnail_image": self.image.pk})

        with self.assertRaises(ValidationError):
            block.clean(value)

    def test_value_contains_thumbnail_url(self):
        block = VideoPlayer()
        value = block.to_python(
            {
                "video_id": "1V0Ax9OIc84",
                "thumbnail_image": self.image.pk,
            }
        )

        self.assertRegex(
            value.thumbnail_url, r"^.*/images/test.*\.original\.png$"
        )

    def test_render(self):
        block = VideoPlayer()
        value = block.to_python(
            {
                "video_id": "1V0Ax9OIc84",
                "thumbnail_image": self.image.pk,
            }
        )

        request = RequestFactory().get("/")
        html = block.render(value, context={"request": request})

        self.assertIn('href="https://www.youtube.com/embed/1V0Ax9OIc84', html)
        self.assertRegex(html, r'src="/f/images/test.*\.original\.png"')


class TestAudioPlayer(TestCase):
    def test_render_audio_player(self):
        block = AudioPlayer()
        fake_file = ContentFile("A boring example mp3")
        fake_file.name = "test.mp3"
        media = Media.objects.create(
            title="Test audio file",
            type="audio",
            duration=100,
            file=File(fake_file),
        )
        value = block.to_python(
            {
                "audio_file": media.pk,
            }
        )

        html = block.render(value)

        self.assertInHTML(
            (
                '<audio class="o-audio-player" controls preload="metadata"'
                '       data-title="Test audio file">'
                '    <source src="/f/media/test.mp3" type="audio/mpeg">'
                "    Your browser does not support this audio player."
                "</audio>"
            ),
            html,
        )

    def test_audio_player_with_video_file_returns_error(self):
        block = AudioPlayer()
        fake_file = ContentFile("Example video")
        fake_file.name = "test.mp4"
        media = Media.objects.create(
            title="Test video file",
            type="video",
            duration=100,
            file=File(fake_file),
        )
        value = block.to_python(
            {
                "audio_file": media.pk,
            }
        )

        html = block.render(value)
        self.assertInHTML("<b>Warning:</b>", html)
