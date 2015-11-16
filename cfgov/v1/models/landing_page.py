from django.db import models

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    FieldRowPanel, TabbedInterface, ObjectList, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import PAGE_TEMPLATE_VAR

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

    content = StreamField([
        ('half_width_link_blob', molecules.HalfWidthLinkBlob()),
        ('image_text_25_75', molecules.ImageText2575()),
        ('image_text_50_50', molecules.ImageText5050()),
        ('well', organisms.Well())
    ], blank=True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('hero'),
        StreamFieldPanel('introduction'),
        StreamFieldPanel('content'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.promote_panels, heading='Promote'),
        ObjectList(CFGOVPage.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request, *args, **kwargs):
        return {
            PAGE_TEMPLATE_VAR: self,
            'self': self,
            'request': request,
        }

    template = '_includes/templates/landing-page/index.html'
