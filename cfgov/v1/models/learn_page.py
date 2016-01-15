import itertools

from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel, FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from .base import CFGOVPage
from . import molecules
from . import organisms


class AbstractLearnPage(CFGOVPage):
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
    date_published = models.DateField()
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

    def elements(self):
        return list(itertools.chain(self.header.stream_data,
                                    self.content.stream_data))


class LearnPage(AbstractLearnPage):
    content = StreamField([
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('well', organisms.Well()),
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', molecules.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table', organisms.Table()),
        ('call_to_action', molecules.CallToAction()),
    ], blank=True)

    edit_handler = AbstractLearnPage.edit_handler

    template = 'learn-page/index.html'


class DocumentDetailPage(AbstractLearnPage):
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', molecules.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table', organisms.Table()),
    ], blank=True)

    edit_handler = AbstractLearnPage.edit_handler

    template = 'document-detail/index.html'
