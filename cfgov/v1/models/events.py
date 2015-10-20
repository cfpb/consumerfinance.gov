import datetime

from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from localflavor.us.models import USStateField

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, FieldRowPanel, TabbedInterface, ObjectList, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import PAGE_TEMPLATE_VAR

from .base import CFGOVPage


class AgendaItemBlock(blocks.StructBlock):
    start_dt = blocks.DateTimeBlock(label="Start", required=False)
    end_dt = blocks.DateTimeBlock(label="End", required=False)
    description = blocks.CharBlock(max_length=100, required=False)
    location = blocks.CharBlock(max_length=100, required=False)
    speakers = blocks.ListBlock(blocks.StructBlock([
        ('name', blocks.CharBlock(required=False)),
        ('url', blocks.URLBlock(required=False)),
        ], icon='user', required=False)
    )

    class Meta:
        icon = 'date'


class EventPage(CFGOVPage):
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
    flickr_url = models.URLField("Flikr URL", blank=True)
    youtube_url = models.URLField("Youtube URL", blank=True)
    live_stream_availability = models.BooleanField("Streaming?", default=False, blank=True)
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
        MultiFieldPanel(CFGOVPage.promote_panels, "Page configuration"),
    ]
    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(venue_panels, heading='Venue Information'),
        ObjectList(agenda_panels, heading='Agenda Information'),
        ObjectList(CFGOVPage.promote_panels, heading='Promote'),
        ObjectList(CFGOVPage.settings_panels, heading='Settings', classname="settings"),
    ])

    parent_page_types = ['v1.EventLandingPage']
    template = 'events/event.html'


class EventLandingPage(CFGOVPage):
    subpage_types = ['EventPage', 'EventArchivePage', 'EventRequestSpeakerPage']

    def get_context(self, request, *args, **kwargs):
        return {
            'events': EventPage.objects.live().filter(start_dt__gt=datetime.datetime.now()),
            PAGE_TEMPLATE_VAR: self,
            'self': self,
            'request': request,
        }

    template = 'events/index.html'

# Importing here solves circular importing for now
from v1.forms import EventsFilterForm


class EventArchivePage(CFGOVPage):
    body = models.TextField(blank=True)

    subpage_types = []

    content_panels = CFGOVPage.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        form = EventsFilterForm(request.GET)
        if form.is_valid():
            # Generates a query by iterating over the zipped collection of
            # tuples. The ordering of query strings is dependent on the
            # ordering of the form fields in the definition of EventsFilterForm.
            final_query = Q()
            for field in zip(['start_dt__gte', 'end_dt__lte', 'tags__name__in'],
                             form.fields):
                if form.cleaned_data.get(field[1]):
                    final_query &= \
                        Q((field[0], form.cleaned_data.get(field[1])))

        # List of paginated events to pass to the template
        events_list = EventPage.objects.live().filter(final_query)
        paginator = Paginator(events_list, 10)
        page = request.GET.get('page')

        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        return {
            'form': form,
            'filters': [field for field in form.fields],
            'events': events,
            PAGE_TEMPLATE_VAR: self,
            'self': self,
            'request': request,
        }

    template = 'events/archive.html'


class EventRequestSpeakerPage(CFGOVPage):
    header = models.CharField(max_length=100)
    intro = models.TextField('Introduction', blank=True)
    subpage_desc = RichTextField('Subpage description', blank=True)
    faq = StreamField([
        ('Heading', blocks.CharBlock(classname="full title")),
        ('Description', blocks.TextBlock()),
        ('QA', blocks.StructBlock([
            ('question', blocks.CharBlock()),
            ('answer', blocks.CharBlock())
        ]))
    ])

    content_panels = CFGOVPage.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('intro', classname="full"),
        FieldPanel('subpage_desc', classname="full"),
        StreamFieldPanel('faq'),
    ]

    template = 'events/request-a-speaker.html'
