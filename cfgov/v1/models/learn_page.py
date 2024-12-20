from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.http import http_date

from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from localflavor.us.models import USStateField

from v1 import blocks as v1_blocks
from v1.atomic_elements import charts, molecules, organisms, schema
from v1.models.base import CFGOVPage
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
    date_published = models.DateField(default=date.today)

    # Configuration tab panels
    settings_panels = Page.settings_panels + [
        MultiFieldPanel(CFGOVPage.promote_panels, "Settings"),
        InlinePanel("categories", label="Categories", max_num=2),
        FieldPanel("tags", heading="Tags"),
        FieldPanel("authors", heading="Authors"),
        FieldPanel("content_owners", heading="Content Owners"),
        FieldPanel("date_published"),
        MultiFieldPanel(
            [
                FieldPanel("language", heading="Language"),
                FieldPanel("english_page"),
            ],
            "Translation",
        ),
    ]

    # This page class cannot be created.
    is_creatable = False
    start_date_field = "date_published"

    @classmethod
    def generate_edit_handler(self, content_panel):
        content_panels = [
            FieldPanel("header"),
            content_panel,
            InlinePanel("footnotes", label="Footnotes"),
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


class LearnPage(AbstractFilterPage):
    content = StreamField(
        [
            ("full_width_text", organisms.FullWidthText()),
            ("info_unit_group", organisms.InfoUnitGroup()),
            ("expandable_group", organisms.ExpandableGroup()),
            ("expandable", organisms.Expandable()),
            ("well", organisms.Well()),
            ("call_to_action", molecules.CallToAction()),
            ("video_player", organisms.VideoPlayer()),
            ("audio_player", organisms.AudioPlayer()),
            (
                "email_signup",
                v1_blocks.EmailSignUpChooserBlock(),
            ),
            ("simple_chart", organisms.SimpleChart()),
            ("table", organisms.Table()),
            ("faq_group", schema.FAQGroup()),
            ("contact_us_table", organisms.ContactUsTable()),
            ("wagtailchart_block", charts.ChartBlock()),
        ],
        blank=True,
    )

    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=FieldPanel("content")
    )
    template = "v1/learn-page/index.html"

    page_description = "Right-hand sidebar, no left-hand sidebar."


class DocumentDetailPage(AbstractFilterPage):
    content = StreamField(
        [
            ("full_width_text", organisms.FullWidthText()),
            ("expandable", organisms.Expandable()),
            ("expandable_group", organisms.ExpandableGroup()),
            ("notification", molecules.Notification()),
            ("simple_chart", organisms.SimpleChart()),
            ("table", organisms.Table()),
            ("crc_table", organisms.ConsumerReportingCompanyTable()),
            ("case_docket_table", organisms.CaseDocketTable()),
            ("wagtailchart_block", charts.ChartBlock()),
        ],
        blank=True,
        block_counts={"case_docket_table": {"max_num": 1}},
    )
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=FieldPanel("content")
    )
    template = "v1/document-detail/index.html"


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
            ("table", organisms.Table()),
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

    # Agenda content fields
    agenda_items = StreamField(
        [("item", AgendaItemBlock())],
        blank=True,
    )

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
                FieldPanel("venue_image_type"),
                FieldPanel("venue_image"),
            ],
            heading="Image",
        ),
        FieldPanel("future_body", heading="Content visible before event"),
        FieldPanel("live_body", heading="Content visible during event"),
        MultiFieldPanel(
            [
                FieldPanel(
                    "archive_body", heading="Content visible after event"
                ),
                FieldPanel("archive_video_id"),
            ],
            heading="Body and information visible after event",
        ),
        FieldPanel("persistent_body", heading="Content visible at all times"),
        MultiFieldPanel(
            [
                FieldPanel("live_stream_availability"),
                FieldPanel("live_video_id"),
                FieldPanel("live_stream_date"),
            ],
            heading="Livestream information",
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
    ]
    # Agenda content tab
    agenda_panels = [
        FieldPanel("agenda_items"),
    ]
    # Promotion panels
    promote_panels = [
        MultiFieldPanel(
            AbstractFilterPage.promote_panels, "Page configuration"
        ),
    ]
    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(venue_panels, heading="Venue Information"),
            ObjectList(agenda_panels, heading="Agenda Information"),
            ObjectList(AbstractFilterPage.sidefoot_panels, heading="Sidebar"),
            ObjectList(
                AbstractFilterPage.settings_panels, heading="Configuration"
            ),
        ]
    )

    template = "v1/events/event.html"
    start_date_field = "start_dt"
    end_date_field = "end_dt"

    @property
    def event_state(self):
        if self.end_dt and self.end_dt < self._cached_now:
            return "past"

        start = min(filter(None, [self.live_stream_date, self.start_dt]))
        if self._cached_now >= start:
            return "present"

        return "future"

    @cached_property
    def location_str(self):
        parts = []

        if self.venue_city and self.venue_state:
            parts.extend([self.venue_city, self.venue_state])
        if self.venue_name:
            parts.append(self.venue_name)
        if self.live_video_id:
            parts.append("Livecast")

        return ", ".join(parts)

    @property
    def page_js(self):
        if (self.live_stream_date and self.event_state == "present") or (
            self.archive_video_id and self.event_state == "past"
        ):
            return super().page_js + ["video-player.js"]

        return super().page_js

    def location_image_url(self, scale="2", size="276x155", zoom="12"):
        if not self.venue_coords:
            self.venue_coords = get_venue_coords(
                self.venue_city, self.venue_state
            )
        api_url = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static"
        static_map_image_url = (
            f"{api_url}/{self.venue_coords},{zoom}/{size}"
            f"?access_token={settings.MAPBOX_ACCESS_TOKEN}"
        )

        return static_map_image_url

    def clean(self):
        super().clean()
        if self.venue_image_type == "image" and not self.venue_image:
            raise ValidationError(
                {"venue_image": 'Required if "Venue image type" is "Image".'}
            )
        if self.live_stream_availability:
            if not self.live_stream_date:
                self.live_stream_date = self.start_dt
            # Make sure live stream doesn't start after event end.
            if self.end_dt and self.live_stream_date >= self.end_dt:
                raise ValidationError(
                    {"live_stream_date": "Cannot be on or after Event End."}
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
        future_changes_at = [
            at for at in changes_at if at and at > self._cached_now
        ]

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
