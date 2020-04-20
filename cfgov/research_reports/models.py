from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface
)
from wagtail.admin.forms.models import WagtailAdminModelFormMetaclass
from wagtail.admin.forms.pages import WagtailAdminPageForm
from wagtail.core.fields import RichTextField
from wagtail.core.models import PageManager

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from v1.models import SublandingFilterablePage
from v1.models.base import CFGOVPage


def get_toc_sections(request, page):
    return [{
        'expanded': False,
        'title': section.header,
        'url': '#' + section.html_id,
        'children': [{
            'title': subsection.sub_header, 'url': '#' + subsection.sub_id
        } for subsection in section.report_subsections.all().order_by('pk')]
    } for section in
        page.report_sections.all().order_by('pk')
        if not section.is_appendix]


def get_toc_appendices(request, page):
    return [{
        'expanded': False,
        'title': section.header,
        'url': '#' + section.html_id,
        'children': [{
            'title': subsection.sub_header, 'url': '#' + subsection.sub_id
        } for subsection in section.report_subsections.all().order_by('pk')]
    } for section in
        page.report_sections.all().order_by('pk')
        if section.is_appendix]


def get_researchers():
    return dict([
        (r.title, r.url) for r in
        SublandingFilterablePage.objects.get(pk=4833).get_children()
    ])


class ReportSection(ClusterableModel):
    header = models.CharField(max_length=200, blank=True)
    html_id = models.CharField(max_length=50, blank=True)
    is_appendix = models.BooleanField(default=False)
    body = RichTextField(blank=True)
    panels = [
        FieldPanel('header'),
        FieldPanel('html_id'),
        FieldPanel('is_appendix'),
        FieldPanel('body'),
        InlinePanel('report_subsections', label='Subsection'),
    ]
    action = ParentalKey('Report',
                         on_delete=models.CASCADE,
                         related_name='report_sections')


class ReportSubSection(models.Model):
    sub_header = models.CharField(max_length=200)
    sub_id = models.CharField(max_length=50, blank=True)
    sub_body = RichTextField(blank=True)
    action = ParentalKey('ReportSection',
                         on_delete=models.CASCADE,
                         related_name='report_subsections')


class AuthorNames(models.Model):
    name = models.CharField(max_length=50)
    action = ParentalKey('Report',
                         on_delete=models.CASCADE,
                         related_name='report_author_names')


class ReportMetaclass(WagtailAdminModelFormMetaclass):
    @classmethod
    def child_form(cls):
        return ReportForm


class ReportForm(WagtailAdminPageForm, metaclass=ReportMetaclass):
    pass


class Report(CFGOVPage):
    base_form_class = ReportForm
    report_type = models.CharField(max_length=100, default='')
    header = models.CharField(max_length=200, default='')
    subheader = models.TextField(blank=True)
    pdf_location = models.CharField(max_length=150, default='')
    footnotes = RichTextField(blank=True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel([
            FieldPanel('report_type'),
            FieldPanel('header'),
            FieldPanel('subheader'),
            InlinePanel(
                'report_author_names',
                label='Author Name',
                min_num=0
            ),
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

    template = 'index.html'

    objects = PageManager()

    def get_context(self, request, *args, **kwargs):
        context = super(Report, self).get_context(request, *args, **kwargs)
        context.update({
            'get_toc_sections': get_toc_sections,
            'get_toc_appendices': get_toc_appendices,
            'get_researchers': get_researchers
        })
        return context
