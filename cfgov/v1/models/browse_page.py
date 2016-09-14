import itertools

from django.db import models

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel, FieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import PAGE_TEMPLATE_VAR
from wagtail.contrib.table_block.blocks import TableBlock

from .base import CFGOVPage
from ..atomic_elements import molecules, organisms
from ..util.util import get_secondary_nav_items
from jobmanager.models import JobListingTable


class BrowsePage(CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', molecules.FeaturedContent()),
    ], blank=True)

    content = StreamField([
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('image_text_50_50_group', organisms.ImageText5050Group()),
        ('half_width_link_blob_group', organisms.HalfWidthLinkBlobGroup()),
        ('third_width_link_blob_group', organisms.ThirdWidthLinkBlobGroup()),
        ('well', organisms.Well()),
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', organisms.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table', organisms.Table(editable=False)),
        ('table_block', organisms.AtomicTableBlock(table_options={'renderer':'html'})),
        ('job_listing_table', JobListingTable()),
    ], blank=True)

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel('secondary_nav_exclude_sibling_pages'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'browse-basic/index.html'

    def add_page_js(self, js):
        super(BrowsePage, self).add_page_js(js)
        js['template'] += ['secondary-navigation.js']

    def full_width_serif(self):
        return true

    def get_context(self, request, *args, **kwargs):
        context = super(BrowsePage, self).get_context(request, *args, **kwargs)
        context.update({'get_secondary_nav_items': get_secondary_nav_items})
        return context
