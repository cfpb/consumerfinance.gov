from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import PageManager
from wagtail.search import index

from modelcluster.fields import ParentalKey

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage


class ReportSection(models.Model):
    section_header = models.CharField(max_length=200, blank=True)
    section_id = models.CharField(max_length=50, blank=True)
    section_body = RichTextField(blank=True)
    action = ParentalKey('v1.ReportSectionsSidenav',
                         on_delete=models.CASCADE,
                         related_name='report_sections')


class ReportSectionsSidenav(CFGOVPage):
    content = StreamField([
      ('full_width_text', organisms.FullWidthText()),
      ('table_block', organisms.AtomicTableBlock(
          table_options={'renderer': 'html'}
      )),
      ('raw_html_block', blocks.RawHTMLBlock(
          label='Raw HTML block'
      )),
    ], blank=True)

    footnotes = StreamField([
      ('full_width_text', organisms.FullWidthText()),
    ], blank=True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('content'),
        MultiFieldPanel([
          InlinePanel(
            'report_sections',
            label='Section',
            min_num=1
          ),
        ], heading='Report Sections'),
        StreamFieldPanel('footnotes')
    ]

    sidefoot_panels = CFGOVPage.sidefoot_panels

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'report/section.html'

    objects = PageManager()

    search_fields = CFGOVPage.search_fields + [
        index.SearchField('content'),
    ]

    @property
    def page_js(self):
        return (
            super(ReportSectionsSidenav, self).page_js + ['report-sidenav.js']
        )
