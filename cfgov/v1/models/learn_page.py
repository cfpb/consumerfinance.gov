from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.http import http_date

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, PageManager
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from localflavor.us.models import USStateField

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage, CFGOVPageManager
from v1.util.events import get_venue_coords


class AbstractFilterPage(CFGOVPage):
    header = StreamField(
        [
            ("article_subheader", blocks.RichTextBlock(icon="form")),
            ("text_introduction", molecules.TextIntroduction()),
            ("item_introduction", organisms.ItemIntroduction()),
            ("notification", molecules.Notification()),
        ],
        blank=True,
    )
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_subheading = models.CharField(max_length=255, null=True, blank=True)
    preview_description = RichTextField(null=True, blank=True)
    secondary_link_url = models.CharField(max_length=500, null=True, blank=True)
    secondary_link_text = models.CharField(max_length=255, null=True, blank=True)
    preview_image = models.ForeignKey(
        "v1.CFGOVImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    date_published = models.DateField(default=date.today)
    date_filed = models.DateField(null=True, blank=True)
    comments_close_by = models.DateField(null=True, blank=True)

    # Configuration tab panels
    settings_panels = [
        MultiFieldPanel(CFGOVPage.promote_panels, "Settings"),
        InlinePanel("categories", label="Categories", max_num=2),
        FieldPanel("tags", "Tags"),
        MultiFieldPanel(
            [
                FieldPanel("preview_title"),
                FieldPanel("preview_subheading"),
                FieldPanel("preview_description"),
                FieldPanel("secondary_link_url"),
                FieldPanel("secondary_link_text"),
                ImageChooserPanel("preview_image"),
            ],
            heading="Page Preview Fields",
            classname="collapsible",
        ),
        FieldPanel("schema_json", "Structured Data"),
        FieldPanel("authors", "Authors"),
        MultiFieldPanel(
            [
                FieldPanel("date_published"),
                FieldPanel("date_filed"),
                FieldPanel("comments_close_by"),
            ],
            "Relevant Dates",
            classname="collapsible",
        ),
        MultiFieldPanel(Page.settings_panels, "Scheduled Publishing"),
        FieldPanel("language", "Language"),
        MultiFieldPanel(CFGOVPage.archive_panels, "Archive"),
    ]

    # This page class cannot be created.
    is_creatable = False

    objects = CFGOVPageManager()

    search_fields = CFGOVPage.search_fields + [index.SearchField("header")]

    @classmethod
    def generate_edit_handler(self, content_panel):
        content_panels = [
            StreamFieldPanel("header"),
            content_panel,
        ]
        return TabbedInterface(
            [
                ObjectList(
                    self.content_panels + content_panels,
                    heading="General Content",
                ),
                ObjectList(CFGOVPage.sidefoot_panels, heading="Sidebar"),
                ObjectList(self.settings_panels, heading="Configuration"),
            ]
        )

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        parent_meta = super().meta_image
        return parent_meta or self.preview_image


class LearnPage(AbstractFilterPage):
    content = StreamField(
        [
            ("full_width_text", organisms.FullWidthText()),
            ("info_unit_group", organisms.InfoUnitGroup()),
            ("expandable_group", organisms.ExpandableGroup()),
            ("contact_expandable_group", organisms.ContactExpandableGroup()),
            ("expandable", organisms.Expandable()),
            ("well", organisms.Well()),
            ("call_to_action", molecules.CallToAction()),
            ("email_signup", organisms.EmailSignUp()),
            ("video_player", organisms.VideoPlayer()),
            ("audio_player", organisms.AudioPlayer()),
            (
                "table_block",
                organisms.AtomicTableBlock(table_options={"renderer": "html"}),
            ),
            ("feedback", v1_blocks.Feedback()),
        ],
        blank=True,
    )

    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=StreamFieldPanel("content")
    )
    template = "learn-page/index.html"

    objects = PageManager()

    search_fields = AbstractFilterPage.search_fields + [index.SearchField("content")]


class DocumentDetailPage(AbstractFilterPage):
    content = StreamField(
        [
            ("full_width_text", organisms.FullWidthText()),
            ("expandable", organisms.Expandable()),
            ("expandable_group", organisms.ExpandableGroup()),
            ("notification", molecules.Notification()),
            (
                "table_block",
                organisms.AtomicTableBlock(table_options={"renderer": "html"}),
            ),
            ("feedback", v1_blocks.Feedback()),
        ],
        blank=True,
    )
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=StreamFieldPanel("content")
    )
    template = "document-detail/index.html"

    objects = PageManager()

    search_fields = AbstractFilterPage.search_fields + [index.SearchField("content")]


class AgendaItemBlock(blocks.StructBlock):
    start_time = blocks.TimeBlock(label="Start", required=False)
    end_time = blocks.TimeBlock(label="End", required=False)
    description = blocks.CharBlock(max_length=100, required=False)
    location = blocks.CharBlock(max_length=100, required=False)
    speakers = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("name", blocks.CharBlock(required=False)),
                ("url", blocks.URLBlock(required=False)),
            ],
            icon="user",
            required=False,
        )
    )

    objects = PageManager()

    class Meta:
        icon = "date"


class EventPage(AbstractFilterPage):
    # General content fields
    body = RichTextField("Subheading", blank=True)
    archive_body = RichTextField(blank=True)
    live_body = RichTextField(blank=True)
    future_body = RichTextField(blank=True)
    persistent_body = StreamField(
        [
            ("content", blocks.RichTextBlock(icon="edit")),
            ("content_with_anchor", molecules.ContentWithAnchor()),
            ("heading", v1_blocks.HeadingBlock(required=False)),
            ("image", molecules.ContentImage()),
            (
                "table_block",
                organisms.AtomicTableBlock(table_options={"renderer": "html"}),
            ),
            (
                "reusable_text",
                v1_blocks.ReusableTextChooserBlock("v1.ReusableText"),
            ),
        ],
        blank=True,
    )
    start_dt = models.DateTimeField("Start")
    end_dt = models.DateTimeField("End", blank=True, null=True)
    future_body = RichTextField(blank=True)
    archive_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    video_transcript = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    speech_transcript = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    flickr_url = models.URLField("Flickr URL", blank=True)
    archive_video_id = models.CharField(
        "YouTube video ID (archive)",
        null=True,
        blank=True,
        max_length=11,
        # This is a reasonable but not official regex for YouTube video IDs.
        # https://webapps.stackexchange.com/a/54448
        validators=[RegexValidator(regex=r"^[\w-]{11}$")],
        help_text=organisms.VideoPlayer.YOUTUBE_ID_HELP_TEXT,
    )
    live_stream_availability = models.BooleanField(
        "Streaming?",
        default=False,
        blank=True,
        help_text="Check if this event will be streamed live. This causes the "
        "event page to show the parts necessary for live streaming.",
    )
    live_video_id = models.CharField(
        "YouTube video ID (live)",
        null=True,
        blank=True,
        max_length=11,
        # This is a reasonable but not official regex for YouTube video IDs.
        # https://webapps.stackexchange.com/a/54448
        validators=[RegexValidator(regex=r"^[\w-]{11}$")],
        help_text=organisms.VideoPlayer.YOUTUBE_ID_HELP_TEXT,
    )
    live_stream_date = models.DateTimeField(
        "Go Live Date",
        blank=True,
        null=True,
        help_text="Enter the date and time that the page should switch from "
        "showing the venue image to showing the live video feed. "
        "This is typically 15 minutes prior to the event start time.",
    )

    # Venue content fields
    venue_coords = models.CharField(max_length=100, blank=True)
    venue_name = models.CharField(max_length=100, blank=True)
    venue_street = models.CharField(max_length=100, blank=True)
    venue_suite = models.CharField(max_length=100, blank=True)
    venue_city = models.CharField(max_length=100, blank=True)
    venue_state = USStateField(blank=True)
    venue_zipcode = models.CharField(max_length=12, blank=True)
    venue_image_type = models.CharField(
        max_length=8,
        choices=(
            ("map", "Map"),
            ("image", "Image (selected below)"),
            ("none", "No map or image"),
        ),
        default="map",
        help_text='If "Image" is chosen here, you must select the image you '
        "want below. It should be sized to 1416x796.",
    )
    venue_image = models.ForeignKey(
        "v1.CFGOVImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    post_event_image_type = models.CharField(
        max_length=16,
        choices=(
            ("placeholder", "Placeholder image"),
            ("image", "Unique image (selected below)"),
        ),
        default="placeholder",
        verbose_name="Post-event image type",
        help_text="Choose what to display after an event concludes. This will "
        'be overridden by embedded video if the "YouTube video ID '
        '(archive)" field on the previous tab is populated. If '
        '"Unique image" is chosen here, you must select the image '
        "you want below. It should be sized to 1416x796.",
    )
    post_event_image = models.ForeignKey(
        "v1.CFGOVImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Agenda content fields
    agenda_items = StreamField([("item", AgendaItemBlock())], blank=True)

    objects = CFGOVPageManager()

    search_fields = AbstractFilterPage.search_fields + [
        index.SearchField("body"),
        index.SearchField("archive_body"),
        index.SearchField("live_video_id"),
        index.SearchField("flickr_url"),
        index.SearchField("archive_video_id"),
        index.SearchField("future_body"),
        index.SearchField("agenda_items"),
    ]

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        FieldPanel("body"),
        FieldRowPanel(
            [
                FieldPanel("start_dt", classname="col6"),
                FieldPanel("end_dt", classname="col6"),
            ]
        ),
        MultiFieldPanel(
            [
                FieldPanel("archive_body"),
                ImageChooserPanel("archive_image"),
                DocumentChooserPanel("video_transcript"),
                DocumentChooserPanel("speech_transcript"),
                FieldPanel("flickr_url"),
                FieldPanel("archive_video_id"),
            ],
            heading="Archive Information",
        ),
        FieldPanel("live_body"),
        FieldPanel("future_body"),
        StreamFieldPanel("persistent_body"),
        MultiFieldPanel(
            [
                FieldPanel("live_stream_availability"),
                FieldPanel("live_video_id"),
                FieldPanel("live_stream_date"),
            ],
            heading="Live Stream Information",
        ),
    ]
    # Venue content tab
    venue_panels = [
        FieldPanel("venue_name"),
        MultiFieldPanel(
            [
                FieldPanel("venue_street"),
                FieldPanel("venue_suite"),
                FieldPanel("venue_city"),
                FieldPanel("venue_state"),
                FieldPanel("venue_zipcode"),
            ],
            heading="Venue Address",
        ),
        MultiFieldPanel(
            [
                FieldPanel("venue_image_type"),
                ImageChooserPanel("venue_image"),
            ],
            heading="Venue Image",
        ),
        MultiFieldPanel(
            [
                FieldPanel("post_event_image_type"),
                ImageChooserPanel("post_event_image"),
            ],
            heading="Post-event Image",
        ),
    ]
    # Agenda content tab
    agenda_panels = [
        StreamFieldPanel("agenda_items"),
    ]
    # Promotion panels
    promote_panels = [
        MultiFieldPanel(AbstractFilterPage.promote_panels, "Page configuration"),
    ]
    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(venue_panels, heading="Venue Information"),
            ObjectList(agenda_panels, heading="Agenda Information"),
            ObjectList(AbstractFilterPage.sidefoot_panels, heading="Sidebar"),
            ObjectList(AbstractFilterPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "events/event.html"

    @property
    def event_state(self):
        if self.end_dt and self.end_dt < self._cached_now:
            return "past"

        start = min(filter(None, [self.live_stream_date, self.start_dt]))
        if self._cached_now >= start:
            return "present"

        return "future"

    @property
    def page_js(self):
        if (self.live_stream_date and self.event_state == "present") or (
            self.archive_video_id and self.event_state == "past"
        ):
            return super().page_js + ["video-player.js"]

        return super().page_js

    def location_image_url(self, scale="2", size="276x155", zoom="12"):
        if not self.venue_coords:
            self.venue_coords = get_venue_coords(self.venue_city, self.venue_state)
        api_url = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static"
        static_map_image_url = "{}/{},{}/{}?access_token={}".format(
            api_url,
            self.venue_coords,
            zoom,
            size,
            settings.MAPBOX_ACCESS_TOKEN,
        )

        return static_map_image_url

    def clean(self):
        super().clean()
        if self.venue_image_type == "image" and not self.venue_image:
            raise ValidationError(
                {"venue_image": 'Required if "Venue image type" is "Image".'}
            )
        if self.post_event_image_type == "image" and not self.post_event_image:
            raise ValidationError(
                {
                    "post_event_image": 'Required if "Post-event image type" is '
                    '"Image".'
                }
            )

    def save(self, *args, **kwargs):
        self.venue_coords = get_venue_coords(self.venue_city, self.venue_state)
        return super().save(*args, **kwargs)

    def get_context(self, request):
        context = super().get_context(request)
        context["event_state"] = self.event_state
        return context

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)

        changes_at = [self.start_dt, self.end_dt, self.live_stream_date]
        future_changes_at = [at for at in changes_at if at and at > self._cached_now]

        if future_changes_at:
            response["Expires"] = http_date(min(future_changes_at).timestamp())

        return response

    @cached_property
    def _cached_now(self):
        """Cached value of now for use during page rendering.

        This property can be used to retrieve a fixed version of "now"
        associated with a single EventPage instance. The first time this
        property is accessed, it will return the current time. Any subsequent
        accesses will return the same time.

        This allows for a consistent timestamp to be used during page render.
        """
        return timezone.now()
