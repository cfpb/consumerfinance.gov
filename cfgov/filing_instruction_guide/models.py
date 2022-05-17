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

from v1.atomic_elements import organisms
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

    content = StreamField(
        [
            ("Fig_Section", organisms.FigSection()),
            ("Fig_Sub_Section", organisms.FigSubSection()),
            ("Fig_Sub_3_Section", organisms.FigSub3Section()),
        ],
        blank=True,
    )

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
                FieldPanel("eyebrow"),
                FieldPanel("page_header"),
                FieldPanel("subheader"),
            ],
            heading="Filing Instruction Guide Header",
        ),
        StreamFieldPanel("content"),
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
            elif section.block_type == "Fig_Sub_Section":
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
                id = f"{ind}."
            if sec_type == "Fig_Sub_Section":
                sub_ind += 1
                sub3_ind = 0
                id = f"{ind}.{sub_ind}."
            if sec_type == "Fig_Sub_3_Section":
                sub3_ind += 1
                id = f"{ind}.{sub_ind}.{sub3_ind}."
            section.value["section_id"] = id

    base_form_class = FIGPageForm
    template = "filing_instruction_guide/index.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update({"toc_headers": self.get_toc_headers(request)})
        return context
