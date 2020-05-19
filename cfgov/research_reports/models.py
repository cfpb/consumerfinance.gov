from datetime import date
import time

from django.db import models
from django.utils.safestring import mark_safe
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import PageManager
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.search import index
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList
)

from v1.models.base import CFGOVPage
from research_reports.parser import parse_document


class ResearchReportPage(CFGOVPage):
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

    # Filterable Post fields - Configuration tab
    preview_title = models.CharField(max_length=255, blank=True)
    preview_subheading = models.CharField(max_length=255, blank=True)
    preview_description = RichTextField(blank=True)
    date_published = models.DateField(default=date.today)

    # Report Content fields
    report_title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    eyebrow = models.CharField(max_length=255, blank=True)
    main_content = models.TextField(blank=True)


    settings_panels = [
        MultiFieldPanel([
            FieldPanel('preview_title'),
            FieldPanel('preview_subheading'),
            FieldPanel('preview_description'),
        ], heading='Page Preview Fields', classname='collapsible'),
    ]

    overview_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
        ], heading="Report Title"),
        MultiFieldPanel([
            DocumentChooserPanel('report_file'),
            FieldPanel('process_report'),
        ], heading='Report Document'),
    ]

    report_panels = [
        MultiFieldPanel([
            FieldPanel('report_title'),
            FieldPanel('subtitle'),
            FieldPanel('eyebrow'),
            FieldPanel('date_published'),
        ], heading='Report Front Page', classname='collapsible'),
        MultiFieldPanel([
            FieldPanel('main_content'),
        ], heading='Report Main Content', classname='collapsible'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(overview_panels, heading='Report Upload'),
        ObjectList(report_panels, heading='Report Content'),
        ObjectList(settings_panels + CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'research-report.html'

    def parse_report_file(self):
        if self.report_file and self.process_report:
            self.process_report = False
            parse_document(self, self.report_file)

    objects = PageManager()

    search_fields = CFGOVPage.search_fields + [
        index.SearchField('report_title'),
        index.SearchField('subtitle')
    ]
