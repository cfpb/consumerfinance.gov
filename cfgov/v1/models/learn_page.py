from datetime import datetime
from localflavor.us.models import USStateField

from django.db import models
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel, FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from . import molecules
from . import organisms
from .base import CFGOVPage
from ..templatetags.share import get_page_state_url
from ..util import util


class AbstractFilterPage(CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('item_introduction', organisms.ItemIntroduction()),
    ], blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_subheading = models.CharField(max_length=255, null=True, blank=True)
    preview_description = RichTextField(null=True, blank=True)
    preview_link_text = models.CharField(max_length=255, null=True, blank=True)
    preview_image = models.ForeignKey(
        'v1.CFGOVImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date_published = models.DateField(default=datetime.now)
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
            FieldPanel('preview_link_text', classname="full"),
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

    class Meta:
        ordering = ('date_published',)

    def related_metadata_tags(self, get_request):
        # Set the tags to correct data format
        tags = {'links': []}
        # From the parent, get the form ids from the BrowseFilterablePage helper method
        # then use the first id since the filterable list on the page will probably
        # have the first id on the page. For more, see v1/models/browse_filterable_page.py line 105.
        parent = self.parent()
        id = util.get_form_id(parent, get_request)
        for tag in self.tags.names():
            tag_link = {'text': tag, 'url': ''}
            if id is not None:
                param = '?filter' + str(id) + '_topics=' + tag
                tag_link['url'] = get_page_state_url({'request': get_request}, parent) + param
            tags['links'].append(tag_link)

        return tags


class LearnPage(AbstractFilterPage):
    content = StreamField([
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('well', organisms.Well()),
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', molecules.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table', organisms.Table()),
        ('call_to_action', molecules.CallToAction()),
    ], blank=True)

    edit_handler = AbstractFilterPage.edit_handler

    template = 'learn-page/index.html'


class DocumentDetailPage(AbstractFilterPage):
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', molecules.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table', organisms.Table()),
    ], blank=True)

    edit_handler = AbstractFilterPage.edit_handler

    template = 'document-detail/index.html'


class AgendaItemBlock(blocks.StructBlock):
    start_dt = blocks.DateTimeBlock(label="Start", required=False)
    end_dt = blocks.DateTimeBlock(label="End", required=False)
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
    body = RichTextField(blank=True)
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
    youtube_url = models.URLField("Youtube URL", blank=True)
    live_stream_availability = models.BooleanField("Streaming?", default=False,
                                                   blank=True)
    live_stream_url = models.URLField("URL", blank=True)
    live_stream_date = models.DateField("Go Live Date", blank=True, null=True)
    # Venue content fields
    venue_name = models.CharField(max_length=100, blank=True)
    venue_street = models.CharField(max_length=100, blank=True)
    venue_suite = models.CharField(max_length=100, blank=True)
    venue_city = models.CharField(max_length=100, blank=True)
    venue_state = USStateField(blank=True)
    venue_zip = models.IntegerField(blank=True, null=True)
    agenda_items = StreamField([('item', AgendaItemBlock())], blank=True)

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
