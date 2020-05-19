from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface
)
from wagtail.admin.forms.pages import WagtailAdminPageForm
from wagtail.admin.forms.models import WagtailAdminModelFormMetaclass
from wagtail.core import blocks
from wagtail.core.fields import RichTextField
from wagtail.core.models import PageManager
from wagtail.search import index

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage


def get_toc_nav_items(request, page):
    return [{
        'expanded': False,
        'title': section.header,
        'url': '#' + section.html_id,
        'children': [{
            'title': subsection.sub_header, 'url': '#' + subsection.sub_id
        } for subsection in section.report_subsections.all().order_by('pk')]
    } for section in page.report_sections.all().order_by('pk')]


class ReportSection(ClusterableModel):
    header = models.CharField(max_length=200, blank=True)
    html_id = models.CharField(max_length=50, blank=True)
    body = RichTextField(blank=True)
    panels = [
        FieldPanel('header'),
        FieldPanel('html_id'),
        FieldPanel('body'),
        InlinePanel('report_subsections', label='Subsection'),
    ]
    action = ParentalKey('v1.ReportSectionsSidenav',
                         on_delete=models.CASCADE,
                         related_name='report_sections')


class ReportSubSection(models.Model):
    sub_header = models.CharField(max_length=200)
    sub_id = models.CharField(max_length=50, blank=True)
    sub_body = RichTextField(blank=True)
    action = ParentalKey('v1.ReportSection',
                         on_delete=models.CASCADE,
                         related_name='report_subsections')


class ReportMetaclass(WagtailAdminModelFormMetaclass):
    @classmethod
    def child_form(cls):
        return ReportForm


class ReportForm(WagtailAdminPageForm, metaclass=ReportMetaclass):
    pass


class ReportSectionsSidenav(CFGOVPage):
    base_form_class = ReportForm
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
        InlinePanel(
          'report_sections',
          label='Section',
          min_num=1
        ),
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
