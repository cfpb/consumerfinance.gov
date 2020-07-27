from django.conf import settings
from django.core import management
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


alpha_map = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_report_parts(is_appendix=False):
    def format(s, *args):
        if(is_appendix):
            return s.format(*[alpha_map[arg] for arg in args])
        else:
            return s.format(*[arg + 1 for arg in args])

    def sec(request, page):
        sections = [section for section in
                    page.report_sections.all().order_by('pk')
                    if section.is_appendix == is_appendix]

        return [{
            'expanded': False,
            'title': section.header,
            'body': section.body,
            'url': format('#section-{}', i),
            'numbering': format('{}: ' if is_appendix else '{}. ', i),
            'children': [{
                'title': subsection.sub_header,
                'body': subsection.sub_body,
                'url': format('#section-{}.{}', i, j),
                'numbering': '' if is_appendix else format('{}.{} ', i, j)
            } for j, subsection in enumerate(
                section.report_subsections.all().order_by('pk')
            )]
        } for i, section in enumerate(sections)]

    return sec


get_report_sections = get_report_parts()
get_report_appendices = get_report_parts(True)


def get_researchers():
    return dict([
        (r.title, r.url) for r in
        SublandingFilterablePage.objects.get(pk=4833).get_children()
    ])


def _get_deploy_environment():
    return getattr(settings, 'DEPLOY_ENVIRONMENT', 'local')


class ReportSection(ClusterableModel):
    header = models.CharField(max_length=200, blank=True)
    is_appendix = models.BooleanField(default=False)
    body = models.TextField(blank=True)
    panels = [
        FieldPanel('header'),
        FieldPanel('is_appendix'),
        FieldPanel('body'),
        InlinePanel('report_subsections', label='Subsection'),
    ]
    report = ParentalKey('ResearchReportPage',
                         on_delete=models.CASCADE,
                         related_name='report_sections')


class ReportSubSection(models.Model):
    sub_header = models.CharField(max_length=200)
    sub_body = models.TextField(blank=True)
    section = ParentalKey('ReportSection',
                          on_delete=models.CASCADE,
                          related_name='report_subsections')


class ReportAuthor(models.Model):
    name = models.CharField(max_length=50)
    report = ParentalKey('ResearchReportPage',
                         on_delete=models.CASCADE,
                         related_name='report_authors')


class ReportMetaclass(WagtailAdminModelFormMetaclass):
    @classmethod
    def child_form(cls):
        return ReportForm


class ReportForm(WagtailAdminPageForm, metaclass=ReportMetaclass):
    pass


class ResearchReportPage(CFGOVPage):
    # Report Upload Fields
    report_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    process_report = models.BooleanField(
        default=False,
        help_text=mark_safe(
            'If this is checked, when you press "save", the system will '
            'read in the report document and use its contents to overwrite '
            'the fields in the "Report Content" tab.'
            '<ul class="help">'
            '    <li>&bull; If you uploaded a new report file for '
            'processing, check this box.</li>'
            '    <li>&bull; If you manually edited fields in the '
            '"Report Content" tab, do not check this box</li>'
            '</ul>'
        )
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
                'report_authors',
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

    def parse_report_file(self):
        if self.report_file and self.process_report:
            deploy_env = _get_deploy_environment()
            if deploy_env == "build":
                # TODO: trigger the jenkins job on Zusa
                pass
            elif deploy_env == "production":
                # TODO: trigger the jenkins job on EXT Jenkins
                pass
            elif deploy_env == 'local' or deploy_env.find('dev') >= 0:
                # if running locally or on a DEV server, run command locally
                management.call_command('parse_research_report', self.id)
            else:
                # deployed to another environment where s3 isn't configured
                # TODO: show a friendly error message to the user
                pass

    def get_context(self, request, *args, **kwargs):
        context = super(ResearchReportPage, self) \
            .get_context(request, *args, **kwargs)
        context.update({
            'get_report_sections': get_report_sections,
            'get_report_appendices': get_report_appendices,
            'get_researchers': get_researchers
        })
        return context
