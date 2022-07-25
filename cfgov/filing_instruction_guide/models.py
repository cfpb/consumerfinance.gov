from datetime import date

from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.fields import StreamField

from filing_instruction_guide.blocks import (
    FigLevel3Subsection,
    FigSection,
    FigSubsection,
)

from v1.models.base import CFGOVPage


class FIGPageForm(WagtailAdminPageForm):
    # Upon saving or previewing the page, assign section IDs
    def save(self, commit=True):
        page = super().save(commit=False)
        page.assign_section_ids()
        if commit:
            page.save()
        return page


class FIGContentPage(CFGOVPage):

    # FIG Header Section Fields
    eyebrow = models.CharField(max_length=100, blank=True)
    page_header = models.CharField(max_length=200, blank=True)
    subheader = models.TextField(blank=True)

    # FIG Version fields
    version_status = models.CharField(
        choices=[
            ("current", "Current"),
            ("old", "Out-of-date"),
            ("archived", "Archived"),
        ],
        default="current",
        max_length=20,
    )
    effective_start_date = models.DateField(
        blank=True, null=True, default=date.today
    )
    effective_end_date = models.DateField(blank=True, null=True)

    content = StreamField(
        [
            ("Fig_Section", FigSection()),
            ("Fig_Subsection", FigSubsection()),
            ("Fig_Level_3_Subsection", FigLevel3Subsection()),
        ],
        blank=True,
    )

    # Main content panel
    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
            ],
            heading="Page Title",
        ),
        MultiFieldPanel(
            [
                FieldPanel("eyebrow"),
                FieldPanel("page_header"),
                FieldPanel("subheader"),
            ],
            heading="Filing Instruction Guide Header",
        ),
        MultiFieldPanel(
            [
                FieldPanel("version_status"),
                FieldPanel("effective_start_date"),
                FieldPanel("effective_end_date"),
            ],
            heading="FIG Version Information",
        ),
        StreamFieldPanel("content"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    def get_toc_headers(self, request):
        toc_headers = []
        parent = None
        for section in self.content:
            header = section.value.get("header")
            id = section.value.get("section_id")
            if section.block_type == "Fig_Section":
                if parent:
                    toc_headers.append(parent)
                parent = {"header": header, "id": id, "children": []}
            elif section.block_type == "Fig_Subsection":
                # if the first block is a subsection instead of a section
                if not parent:
                    parent = {"header": "", "id": "", "children": []}
                parent["children"].append({"header": header, "id": id})
        toc_headers.append(parent)
        return toc_headers

    def assign_section_ids(self):
        ind = sub_ind = sub3_ind = 0
        for section in self.content:
            id = ""
            sec_type = section.block_type
            if sec_type == "Fig_Section":
                ind += 1
                sub_ind = 0
                sub3_ind = 0
                id = f"{ind}"
            if sec_type == "Fig_Subsection":
                sub_ind += 1
                sub3_ind = 0
                id = f"{ind}.{sub_ind}"
            if sec_type == "Fig_Level_3_Subsection":
                sub3_ind += 1
                id = f"{ind}.{sub_ind}.{sub3_ind}"
            section.value["section_id"] = id

    base_form_class = FIGPageForm
    template = "filing_instruction_guide/index.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update({"toc_headers": self.get_toc_headers(request)})
        return context
