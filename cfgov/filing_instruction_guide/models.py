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
