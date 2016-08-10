from datetime import date
from localflavor.us.models import USStateField

from django.db import models
from django.core.validators import RegexValidator
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel, FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from ..atomic_elements import molecules, organisms
from .base import CFGOVPage, CFGOVPageManager


class AbstractFilterPage(CFGOVPage):
    header = StreamField([
        ('article_subheader', blocks.RichTextBlock(icon='form')),
        ('text_introduction', molecules.TextIntroduction()),
        ('item_introduction', organisms.ItemIntroduction()),
    ], blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_subheading = models.CharField(max_length=255, null=True, blank=True)
    preview_description = RichTextField(null=True, blank=True)
    secondary_link_url = models.CharField(max_length=500, null=True, blank=True)
    secondary_link_text = models.CharField(max_length=255, null=True, blank=True)
    preview_image = models.ForeignKey(
        'v1.CFGOVImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date_published = models.DateField(default=date.today)
    date_filed = models.DateField(null=True, blank=True)
    comments_close_by = models.DateField(null=True, blank=True)

    # General content tab panels
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    # Configuration tab panels
    settings_panels = [
        MultiFieldPanel(Page.promote_panels, 'Settings'),
        MultiFieldPanel([
            FieldPanel('preview_title', classname="full"),
            FieldPanel('preview_subheading', classname="full"),
            FieldPanel('preview_description', classname="full"),
            FieldPanel('secondary_link_url', classname="full"),
            FieldPanel('secondary_link_text', classname="full"),
            ImageChooserPanel('preview_image'),
        ], heading='Page Preview Fields', classname='collapsible collapsed'),
        MultiFieldPanel([
            FieldPanel('date_published'),
            FieldPanel('date_filed'),
            FieldPanel('comments_close_by'),
        ], 'Relevant Dates', classname='collapsible'),
        FieldPanel('tags', 'Tags'),
        FieldPanel('authors', 'Authors'),
        InlinePanel('categories', label="Categories", max_num=2),
        MultiFieldPanel(Page.settings_panels, 'Scheduled Publishing'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(settings_panels, heading='Configuration'),
    ])

    # This page class cannot be created.
    is_creatable = False

    objects = CFGOVPageManager()


class LearnPage(AbstractFilterPage):
    content = StreamField([
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('well', organisms.Well()),
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', organisms.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table', organisms.Table()),
        ('call_to_action', molecules.CallToAction()),
    ], blank=True)

    edit_handler = AbstractFilterPage.edit_handler

    template = 'learn-page/index.html'


class DocumentDetailPage(AbstractFilterPage):
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', organisms.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table', organisms.Table()),
    ], blank=True)

    edit_handler = AbstractFilterPage.edit_handler

    template = 'document-detail/index.html'


class AgendaItemBlock(blocks.StructBlock):
    start_time = blocks.TimeBlock(label="Start", required=False)
    end_time = blocks.TimeBlock(label="End", required=False)
    description = blocks.CharBlock(max_length=100, required=False)
    location = blocks.CharBlock(max_length=100, required=False)
    speakers = blocks.ListBlock(blocks.StructBlock([
        ('name', blocks.CharBlock(required=False)),
        ('url', blocks.URLBlock(required=False)),
    ], icon='user', required=False))

    class Meta:
        icon = 'date'


class EventPage(AbstractFilterPage):
    # General content fields
    body = RichTextField('Subheading', blank=True)
    archive_body = RichTextField(blank=True)
    live_body = RichTextField(blank=True)
    future_body = RichTextField(blank=True)
    start_dt = models.DateTimeField("Start", blank=True, null=True)
    end_dt = models.DateTimeField("End", blank=True, null=True)
    future_body = RichTextField(blank=True)
    archive_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    video_transcript = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    speech_transcript = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    flickr_url = models.URLField("Flickr URL", blank=True)
    youtube_url = models.URLField("Youtube URL", blank=True,
    help_text="Format: https://www.youtube.com/embed/video_id. It can be obtained by clicking on Share > Embed on Youtube.",
    validators=[ RegexValidator(regex='^https?:\/\/www\.youtube\.com\/embed\/.*$')])

    live_stream_availability = models.BooleanField("Streaming?", default=False,
                                                   blank=True)
    live_stream_url = models.URLField("URL", blank=True,
    help_text="Format: https://www.ustream.tv/embed/video_id.  It can be obtained by following the instructions listed here: " \
    "https://support.ustream.tv/hc/en-us/articles/207851917-How-to-embed-a-stream-or-video-on-your-site",
    validators=[ RegexValidator(regex='^https?:\/\/www\.ustream\.tv\/embed\/.*$')])
    live_stream_date = models.DateTimeField("Go Live Date", blank=True, null=True)
    # Venue content fields
    venue_name = models.CharField(max_length=100, blank=True)
    venue_street = models.CharField(max_length=100, blank=True)
    venue_suite = models.CharField(max_length=100, blank=True)
    venue_city = models.CharField(max_length=100, blank=True)
    venue_state = USStateField(blank=True)
    venue_zip = models.IntegerField(blank=True, null=True)
    agenda_items = StreamField([('item', AgendaItemBlock())], blank=True)

    objects = CFGOVPageManager()

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        FieldPanel('body', classname="full"),
        FieldRowPanel([
            FieldPanel('start_dt', classname="col6"),
            FieldPanel('end_dt', classname="col6"),
        ]),
        MultiFieldPanel([
            FieldPanel('archive_body', classname="full"),
            ImageChooserPanel('archive_image'),
            DocumentChooserPanel('video_transcript'),
            DocumentChooserPanel('speech_transcript'),
            FieldPanel('flickr_url'),
            FieldPanel('youtube_url'),
        ], heading='Archive Information'),
        FieldPanel('live_body', classname="full"),
        FieldPanel('future_body', classname="full"),
        MultiFieldPanel([
            FieldPanel('live_stream_availability'),
            FieldPanel('live_stream_url'),
            FieldPanel('live_stream_date'),
        ], heading='Live Stream Information'),
    ]
    # Venue content tab
    venue_panels = [
        FieldPanel('venue_name'),
        MultiFieldPanel([
            FieldPanel('venue_street'),
            FieldPanel('venue_suite'),
            FieldPanel('venue_city'),
            FieldPanel('venue_state'),
            FieldPanel('venue_zip'),
        ], heading='Venue Address'),
    ]
    # Agenda content tab
    agenda_panels = [
        StreamFieldPanel('agenda_items'),
    ]
    # Promotion panels
    promote_panels = [
        MultiFieldPanel(AbstractFilterPage.promote_panels,
                        "Page configuration"),
    ]
    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(venue_panels, heading='Venue Information'),
        ObjectList(agenda_panels, heading='Agenda Information'),
        ObjectList(AbstractFilterPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(AbstractFilterPage.settings_panels, heading='Configuration'),
    ])

    template = 'events/event.html'
