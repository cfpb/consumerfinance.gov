import itertools

from django.db import models

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel, FieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import PAGE_TEMPLATE_VAR

from .base import CFGOVPage
from . import molecules
from . import organisms
from ..util.util import get_secondary_nav_items

class BrowsePage(CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', molecules.FeaturedContent()),
    ], blank=True)

    content = StreamField([
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('image_text_50_50_group', organisms.ImageText5050Group()),
        ('half_width_link_blob_group', organisms.HalfWidthLinkBlobGroup()),
        ('well', organisms.Well()),
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', molecules.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table', organisms.Table()),
    ], blank=True)
    secondary_nav_order = models.IntegerField(default=1)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    settings_panels = CFGOVPage.settings_panels + [
        FieldPanel('secondary_nav_order'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(settings_panels, heading='Configuration'),
    ])

    template = 'browse-basic/index.html'

    def elements(self):
        return list(itertools.chain(self.content.stream_data))

    def full_width_serif(self):
        return true

    def get_context(self, request, *args, **kwargs):
        context = super(BrowsePage, self).get_context(request, *args, **kwargs)
        context.update({'get_secondary_nav_items': get_secondary_nav_items})
        return context
