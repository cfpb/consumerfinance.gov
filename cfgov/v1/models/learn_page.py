from datetime import date

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, ObjectList,
    StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, PageManager
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

import requests
from localflavor.us.models import USStateField

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage, CFGOVPageManager


class AbstractFilterPage(CFGOVPage):
    header = StreamField([
        ('article_subheader', blocks.RichTextBlock(icon='form')),
        ('text_introduction', molecules.TextIntroduction()),
        ('item_introduction', organisms.ItemIntroduction()),
    ], blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_subheading = models.CharField(
        max_length=255, null=True, blank=True)
    preview_description = RichTextField(null=True, blank=True)
    secondary_link_url = models.CharField(
        max_length=500, null=True, blank=True)
    secondary_link_text = models.CharField(
        max_length=255, null=True, blank=True)
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

    # Configuration tab panels
    settings_panels = [
        MultiFieldPanel(CFGOVPage.promote_panels, 'Settings'),
        InlinePanel('categories', label="Categories", max_num=2),
        FieldPanel('tags', 'Tags'),
        MultiFieldPanel([
            FieldPanel('preview_title', classname="full"),
            FieldPanel('preview_subheading', classname="full"),
            FieldPanel('preview_description', classname="full"),
            FieldPanel('secondary_link_url', classname="full"),
            FieldPanel('secondary_link_text', classname="full"),
            ImageChooserPanel('preview_image'),
        ], heading='Page Preview Fields', classname='collapsible'),
        FieldPanel('authors', 'Authors'),
        MultiFieldPanel([
            FieldPanel('date_published'),
            FieldPanel('date_filed'),
            FieldPanel('comments_close_by'),
        ], 'Relevant Dates', classname='collapsible'),
        MultiFieldPanel(Page.settings_panels, 'Scheduled Publishing'),
        FieldPanel('language', 'Language'),
    ]

    # This page class cannot be created.
    is_creatable = False

    objects = CFGOVPageManager()

    search_fields = CFGOVPage.search_fields + [
        index.SearchField('header')
    ]

    @classmethod
    def generate_edit_handler(self, content_panel):
        content_panels = [
            StreamFieldPanel('header'),
            content_panel,
        ]
        return TabbedInterface([
            ObjectList(self.content_panels + content_panels,
                       heading='General Content'),
            ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
            ObjectList(self.settings_panels, heading='Configuration'),
        ])

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        parent_meta = super(AbstractFilterPage, self).meta_image
        return parent_meta or self.preview_image


class LearnPage(AbstractFilterPage):
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('info_unit_group_25_75_only', organisms.InfoUnitGroup2575Only()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('expandable', organisms.Expandable()),
        ('well', organisms.Well()),
        ('call_to_action', molecules.CallToAction()),
        ('email_signup', organisms.EmailSignUp()),
        ('video_player', organisms.VideoPlayer()),
        ('table_block', organisms.AtomicTableBlock(
            table_options={'renderer': 'html'}
        )),
        ('feedback', v1_blocks.Feedback()),
    ], blank=True)
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=StreamFieldPanel('content')
    )
    template = 'learn-page/index.html'

    objects = PageManager()

    search_fields = AbstractFilterPage.search_fields + [
        index.SearchField('content')
    ]


class DocumentDetailPage(AbstractFilterPage):
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', organisms.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table_block', organisms.AtomicTableBlock(
            table_options={'renderer': 'html'})),
        ('feedback', v1_blocks.Feedback()),
    ], blank=True)
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=StreamFieldPanel('content')
    )
    template = 'document-detail/index.html'

    objects = PageManager()

    search_fields = AbstractFilterPage.search_fields + [
        index.SearchField('content')
    ]


class AgendaItemBlock(blocks.StructBlock):
    start_time = blocks.TimeBlock(label="Start", required=False)
    end_time = blocks.TimeBlock(label="End", required=False)
    description = blocks.CharBlock(max_length=100, required=False)
    location = blocks.CharBlock(max_length=100, required=False)
    speakers = blocks.ListBlock(blocks.StructBlock([
        ('name', blocks.CharBlock(required=False)),
        ('url', blocks.URLBlock(required=False)),
    ], icon='user', required=False))

    objects = PageManager()

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
    youtube_url = models.URLField(
        "Youtube URL",
        blank=True,
        help_text="Format: https://www.youtube.com/embed/video_id. "
                  "It can be obtained by clicking on Share > "
                  "Embed on Youtube.",
        validators=[
            RegexValidator(regex=r'^https?:\/\/www\.youtube\.com\/embed\/.*$')
        ]
    )

    live_stream_availability = models.BooleanField(
        "Streaming?",
        default=False,
        blank=True
    )
    live_stream_url = models.URLField(
        "URL",
        blank=True,
        help_text="Format: https://www.youtube.com/embed/video_id."
    )
    live_stream_date = models.DateTimeField(
        "Go Live Date",
        blank=True,
        null=True
    )
    # Venue content fields
    venue_coords = models.CharField(max_length=100, blank=True)
    venue_name = models.CharField(max_length=100, blank=True)
    venue_street = models.CharField(max_length=100, blank=True)
    venue_suite = models.CharField(max_length=100, blank=True)
    venue_city = models.CharField(max_length=100, blank=True)
    venue_state = USStateField(blank=True)
    venue_zip = models.IntegerField(blank=True, null=True)
    agenda_items = StreamField([('item', AgendaItemBlock())], blank=True)

    objects = CFGOVPageManager()

    search_fields = AbstractFilterPage.search_fields + [
        index.SearchField('body'),
        index.SearchField('archive_body'),
        index.SearchField('live_stream_url'),
        index.SearchField('flickr_url'),
        index.SearchField('youtube_url'),
        index.SearchField('future_body'),
        index.SearchField('agenda_items')
    ]

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
        ObjectList(AbstractFilterPage.sidefoot_panels,
                   heading='Sidebar'),
        ObjectList(AbstractFilterPage.settings_panels,
                   heading='Configuration'),
    ])

    template = 'events/event.html'

    @property
    def page_js(self):
        return super(EventPage, self).page_js + ['video-player.js']

    def get_venue_coords(self):
        # Default to Washington DC coordinates
        venue_coords = '-77.039628,38.898238'

        if not self.venue_city or not self.venue_state:
            return venue_coords

        location = '{} {}'.format(self.venue_city, self.venue_state)
        api = 'https://api.mapbox.com/geocoding/v5/mapbox.places-permanent/'
        location_api_url = api + location + '.json'

        params = {'access_token': settings.MAPBOX_ACCESS_TOKEN}
        response = requests.get(location_api_url, params=params)

        if response.status_code != 200:
            return venue_coords

        try:
            geo_data = response.json()
            coordinates = geo_data['features'][0]['geometry']['coordinates']
            venue_coords = str(coordinates[0]) + ',' + str(coordinates[1])
        except KeyError:
            pass

        return venue_coords

    def location_image_url(self, scale='2', size='276x155', zoom='12'):
        if not self.venue_coords:
            self.venue_coords = self.get_venue_coords()
        api_url = 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/static'
        static_map_image_url = '{}/{},{}/{}?access_token={}'.format(
            api_url,
            self.venue_coords,
            zoom,
            size,
            settings.MAPBOX_ACCESS_TOKEN
        )

        return static_map_image_url

    def save(self, *args, **kwargs):
        self.venue_coords = self.get_venue_coords()
        return super(EventPage, self).save(*args, **kwargs)
