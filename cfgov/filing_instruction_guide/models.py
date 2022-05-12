from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import StreamField

from v1.atomic_elements import organisms
from v1.models.base import CFGOVPage



def get_toc_headers(request, self):
    toc_headers = []
    for section in self.content:
        header = section.value.get("header")
        id = section.value.get("section_id")
        if section.block_type == "Fig_Section":
            toc_headers.append({"header": header, "id": id, "level": 1})
        elif section.block_type == "Fig_Sub_Section":
            toc_headers.append({"header": header, "id": id, "level": 2})
        return toc_headers


class FIGContentPage(CFGOVPage):

    # FIG Header Section Fields
    eyebrow = models.CharField(max_length=100, blank=True)
    page_header = models.CharField(max_length=200, blank=True)
    subheader = models.TextField(blank=True)

    content = StreamField([
        ("Fig_Section", organisms.FigSection()),
        ("Fig_Sub_Section", organisms.FigSubSection()),
        ("Fig_Sub_3_Section", organisms.FigSub3Section()),
    ], blank=True)

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

    def assign_section_ids(self):
        print("assign section IDs here ????? ****")


    template = "filing_instruction_guide/index.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update( { "get_sections": get_toc_headers(request, self) })
        return context
