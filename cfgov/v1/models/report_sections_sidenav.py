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


def get_toc_nav_items(request, page):
    return [{'title': section.section_header, 'url': '#' + section.section_id} for
            section in page.report_sections.all().order_by('pk')]

class ReportSection(models.Model):
    section_header = models.CharField(max_length=200, blank=True)
    section_id = models.CharField(max_length=50, blank=True)
    section_body = RichTextField(blank=True)
    action = ParentalKey('v1.ReportSectionsSidenav',
                         on_delete=models.CASCADE,
                         related_name='report_sections')


class ReportSectionsSidenav(CFGOVPage):
    header = models.CharField(max_length=200, default='')
    subheader = RichTextField(blank=True)
    pdf_location = models.CharField(max_length=150, default='')
    footnotes = RichTextField(blank = True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel([
          FieldPanel('header'),
          FieldPanel('subheader'),
          FieldPanel('pdf_location')
        ], heading='Report Header'),
        MultiFieldPanel([
          InlinePanel(
            'report_sections',
            label='Section',
            min_num=1
          ),
        ], heading='Report Sections'),
        FieldPanel('footnotes')
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

    @property
    def page_js(self):
        return (
            super(ReportSectionsSidenav, self).page_js + ['report-sidenav.js']
        )

    def get_context(self, request, *args, **kwargs):
        context = super(ReportSectionsSidenav, self).get_context(request, *args, **kwargs)
        context.update({
            'get_toc_nav_items': get_toc_nav_items
        })
        return context
