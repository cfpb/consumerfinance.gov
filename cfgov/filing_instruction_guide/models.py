from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from v1.atomic_elements import organisms
from v1.models.base import CFGOVPage


alpha_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_report_parts(is_appendix=False):
    def format(s, *args):
        if is_appendix:
            return s.format(*[alpha_map[arg] for arg in args])
        else:
            return s.format(*[arg + 1 for arg in args])

    def sec(request, page):
        sections = [
            section
            for section in page.report_sections.all().order_by("pk")
            if section.is_appendix == is_appendix
        ]

        return [
            {
                "expanded": False,
                "title": section.section_title,
                "body": section.section_content,
                "id": format("section-{}", i),
                "numbering": format("{}: " if is_appendix else "{}. ", i),
                "children": [
                    {
                        "title": subsection.sub_section_title,
                        "body": subsection.sub_section_content,
                        "id": format("section-{}.{}", i, j),
                        "numbering": ""
                        if is_appendix
                        else format("{}.{} ", i, j),
                        "children": [
                            {
                                "title": section3.header,
                                "body": section3.body,
                                "id": format("section-{}.{}.{}", i, j, k),
                                "numbering": ""
                                if is_appendix
                                else format("{}.{}.{} ", i, j, k),
                            }
                            for k, section3 in enumerate(
                                subsection.report_sections_level_three.all().order_by(
                                    "pk"
                                )
                            )
                        ],
                    }
                    for j, subsection in enumerate(
                        section.report_subsections.all().order_by("pk")
                    )
                ],
            }
            for i, section in enumerate(sections)
        ]

    return sec


get_report_sections = get_report_parts()
get_report_appendices = get_report_parts(True)


class ReportSection(ClusterableModel):
    section_title = models.CharField(max_length=200, blank=True)
    is_appendix = models.BooleanField(default=False)
    section_content = StreamField(
        [("full_width_text", organisms.FullWidthText())], blank=True
    )
    panels = [
        FieldPanel("section_title"),
        FieldPanel("is_appendix"),
        StreamFieldPanel("section_content"),
        InlinePanel("report_subsections", label="Subsection"),
    ]
    report = ParentalKey(
        "FIGContentPage",
        on_delete=models.CASCADE,
        related_name="report_sections",
    )


class ReportSubSection(ClusterableModel):
    sub_section_title = models.CharField(max_length=200)
    sub_section_content = StreamField(
        [("full_width_text", organisms.FullWidthText())], blank=True
    )
    panels = [
        FieldPanel("sub_section_title"),
        StreamFieldPanel("sub_section_content"),
        InlinePanel(
            "report_sections_level_three", label="Section Level Three"
        ),
    ]
    section = ParentalKey(
        "ReportSection",
        on_delete=models.CASCADE,
        related_name="report_subsections",
    )


class ReportSectionLevelThree(models.Model):
    header = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    subsection = ParentalKey(
        "ReportSubSection",
        on_delete=models.CASCADE,
        related_name="report_sections_level_three",
    )


class FIGContentPage(CFGOVPage):

    # FIG Header Section Fields
    report_type = models.CharField(max_length=100, blank=True)
    page_header = models.CharField(max_length=200, blank=True)
    subheader = models.TextField(blank=True)

    # Report upload tab
    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
            ],
            heading="Page Title",
        ),
        MultiFieldPanel(
            [
                FieldPanel("report_type"),
                FieldPanel("page_header"),
                FieldPanel("subheader"),
            ],
            heading="Filing Instruction Guide Header",
        ),
        InlinePanel(
            "report_sections",
            label="Filing Instruction Guide Sections",
            min_num=0,
        ),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(
                content_panels, heading="Filing Instruction Guide Content"
            ),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "filing_instruction_guide/index.html"

    objects = PageManager()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(
            {
                "report_sections": get_report_sections(request, self),
                "report_appendices": get_report_appendices(request, self),
            }
        )
        return context
