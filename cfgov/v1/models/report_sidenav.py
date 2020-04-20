from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager
from wagtail.search import index

from youth_employment.blocks import YESChecklist

from data_research.blocks import (
    ConferenceRegistrationForm, MortgageDataDownloads
)
from jobmanager.blocks import JobListingTable
from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage

def get_toc_nav_items(request, current_page):
    nav_items = [
        {
          'title': 'Introduction',
          'url': '#introduction'
        },
        {
          'title': 'Public Record Information on Reports and Credit Scores',
          'url': '#public-record'
        },
        {
          'title': 'Credit Scores and Consumers’ credit performance',
          'url': '#credit-scores'
        },
        {
          'title': 'Summary and Conclusion',
          'url': '#summary'
        }
    ]
    return nav_items


class ReportSidenav(CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', organisms.FeaturedContent()),
    ], blank=True)

    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('info_unit_group', organisms.InfoUnitGroup()),
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
        ('bureau_structure', organisms.BureauStructure()),
        ('yes_checklist', YESChecklist()),
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

    template = 'report/index.html'

    objects = PageManager()

    search_fields = CFGOVPage.search_fields + [
        index.SearchField('content'),
        index.SearchField('header')
    ]

    @property
    def page_js(self):
        return (
            super(ReportSidenav, self).page_js + ['report-sidenav.js']
        )

    def get_context(self, request, *args, **kwargs):
        context = super(ReportSidenav, self).get_context(request, *args, **kwargs)
        context.update({
            'get_toc_nav_items': get_toc_nav_items
        })
        return context
