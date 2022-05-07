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


def build_sections(request, self):
    sections = []

    for i, block in enumerate(self.content, start=1):
        val = block.value
        header = val.get("header")
        content = val.get("content")
        sections.append({"id": f"{i}", "name": header})

        j = 1
        for num in range(len(content)):
            val = content[num]
            if val.block_type == "subsection":
                h2 = val.value.get("header")
                c2 = val.value.get("content")
                sections.append({"id": f"{i}.{j}", "name": h2})

                k = 1
                for num in range(len(c2)):
                    val = c2[num]
                    if val.block_type == "level_three_section":
                        h3 = val.value.get("header")
                        sections.append({"id": f"{i}.{j}.{k}", "name": h3})
                        k += 1
                j += 1

    return sections


# Template page
class FIGContentPage(CFGOVPage):

    # FIG Header Section Fields
    report_type = models.CharField(max_length=100, blank=True)
    page_header = models.CharField(max_length=200, blank=True)
    subheader = models.TextField(blank=True)

    # FIG Content Section Fields
    content = StreamField(
        [("Fig_Section", organisms.FigSection())], blank=True
    )

    # Wagtail Content Panels
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

    template = "filing_instruction_guide/index.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update({"sections": build_sections(request, self)})

        return context
