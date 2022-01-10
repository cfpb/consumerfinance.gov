from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager
from wagtail.search import index

from data_research.blocks import (
    ConferenceRegistrationForm, MortgageDataDownloads
)
from jobmanager.blocks import JobListingTable
from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage
from v1.util.util import get_secondary_nav_items
from youth_employment.blocks import YESChecklist


class BrowsePage(CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', organisms.FeaturedContent()),
        ('notification', molecules.Notification()),
    ], blank=True)

    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('simple_chart', organisms.SimpleChart()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('expandable', organisms.Expandable()),
        ('well', organisms.Well()),
        ('video_player', organisms.VideoPlayer()),
        ('snippet_list', organisms.ResourceList()),
        ('table_block', organisms.AtomicTableBlock(
            table_options={'renderer': 'html'}
        )),
        ('feedback', v1_blocks.Feedback()),
        ('raw_html_block', blocks.RawHTMLBlock(
            label='Raw HTML block'
        )),
        ('conference_registration_form', ConferenceRegistrationForm()),
        ('chart_block', organisms.ChartBlock()),
        ('mortgage_chart_block', organisms.MortgageChartBlock()),
        ('mortgage_map_block', organisms.MortgageMapBlock()),
        ('mortgage_downloads_block', MortgageDataDownloads()),
        ('data_snapshot', organisms.DataSnapshot()),
        ('job_listing_table', JobListingTable()),
        ('yes_checklist', YESChecklist()),
        ('erap_tool', v1_blocks.RAFToolBlock()),
        ('raf_tool', v1_blocks.RAFTBlock())
    ], blank=True)

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    share_and_print = models.BooleanField(
        default=False,
        help_text="Include share and print buttons above page content."
    )

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        FieldPanel('share_and_print'),
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

    objects = PageManager()

    search_fields = CFGOVPage.search_fields + [
        index.SearchField('content'),
        index.SearchField('header')
    ]

    @property
    def page_js(self):
        return (
            super(BrowsePage, self).page_js + ['secondary-navigation.js']
        )

    def get_context(self, request, *args, **kwargs):
        context = super(BrowsePage, self).get_context(request, *args, **kwargs)
        context.update({
            'get_secondary_nav_items': get_secondary_nav_items
        })
        return context
