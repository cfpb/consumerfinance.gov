from django.db import models

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    FieldRowPanel, TabbedInterface, ObjectList, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page, PAGE_TEMPLATE_VAR

from .base import CFGOVPage
from . import molecules
from . import organisms


class LandingPage(CFGOVPage):
    hero = StreamField([
        ('hero', molecules.Hero())
    ], blank=True)

    introduction = StreamField([
        ('text_introduction', molecules.TextIntroduction())
    ], blank=True)

    image_text_25_75_group_header = models.CharField(max_length=100, blank=True, verbose_name="Group Header")
    image_text_25_75_content = StreamField([
        ('image_text_25_75', molecules.ImageText2575())
    ], blank=True, verbose_name="content")

    image_text_50_50_group_header = models.CharField(max_length=100, blank=True, verbose_name="Group Header")
    image_text_50_50_content = StreamField([
        ('image_text_50_50', molecules.ImageText5050())
    ], blank=True, verbose_name="content")

    half_width_link_blob_group_header = models.CharField(max_length=100, blank=True, verbose_name="Group Header")
    half_width_link_blob_content = StreamField([
        ('half_width_link_blob', molecules.HalfWidthLinkBlob())
    ], blank=True, verbose_name="content")

    wells = StreamField([
        ('well', organisms.Well())
    ], blank=True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('hero'),
        StreamFieldPanel('introduction'),
        MultiFieldPanel([
            FieldPanel('image_text_50_50_group_header'),
            StreamFieldPanel('image_text_50_50_content'),
        ], heading='Image Text 50 50'),
        MultiFieldPanel([
            FieldPanel('image_text_25_75_group_header'),
            StreamFieldPanel('image_text_25_75_content'),
        ], heading='Image Text 25 75'),
        StreamFieldPanel('wells'),
        MultiFieldPanel([
            FieldPanel('half_width_link_blob_group_header'),
            StreamFieldPanel('half_width_link_blob_content'),
        ], heading='Half Width Link Blob'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request, *args, **kwargs):
        return {
            PAGE_TEMPLATE_VAR: self,
            'self': self,
            'request': request,
        }

    template = 'landing-page/index.html'
