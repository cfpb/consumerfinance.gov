from django.db import models
from django.utils.safestring import mark_safe

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface
)
from wagtail.admin.forms.models import WagtailAdminModelFormMetaclass
from wagtail.admin.forms.pages import WagtailAdminPageForm
from wagtail.core.models import PageManager
from wagtail.documents.edit_handlers import DocumentChooserPanel

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
    body = models.TextField(blank=True)
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
    sub_body = models.TextField(blank=True)
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
    # Report Upload Fields
    report_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    process_report = models.BooleanField(default=False,
            help_text=mark_safe(
                'If this is checked, when you press "save", the system will '
                'read in the report document and use its contents to overwrite '
                'the fields in the "Report Content" tab.'
                '<ul class="help">'
                '    <li>&bull; If you uploaded a new report file for processing, check this box.</li>'
                '    <li>&bull; If you manually edited fields in the "Report Content" tab, do not check this box</li>'
                '</ul>')
            )

    # Report Upload Tabs
    upload_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
        ], heading="Report Title"),
        MultiFieldPanel([
            DocumentChooserPanel('report_file'),
            FieldPanel('process_report'),
        ], heading='Report Document'),
    ]

    # Report Content Fields
    base_form_class = ReportForm
    report_type = models.CharField(max_length=100, blank=True)
    header = models.CharField(max_length=200, blank=True)
    subheader = models.TextField(blank=True)
    pdf_location = models.CharField(max_length=150, blank=True)
    footnotes = models.TextField(blank=True)

    # Report content tab
    content_panels = [
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
            min_num=0
        ),
        FieldPanel('footnotes')
    ]

    sidefoot_panels = CFGOVPage.sidefoot_panels

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(upload_panels, heading='Report Upload'),
        ObjectList(content_panels, heading='Report Content'),
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
