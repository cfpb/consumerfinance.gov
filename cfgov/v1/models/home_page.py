from django.db import models

from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import StreamField

from v1.models.base import CFGOVPage


class HomePage(CFGOVPage):
    hero_heading = models.TextField(
        blank=True,
        null=True,
    )

    hero_heading_continued = models.TextField(
        blank=True,
        null=True,
    )

    hero_image = models.TextField(
        blank=True,
        null=True,
    )

    topics_heading = models.TextField(
        blank=True,
        null=True,
    )

    breakout_cards_heading = models.TextField(
        blank=True,
        null=True,
    )

    class HighlightItemBlock(blocks.StructBlock):
        img_src = blocks.CharBlock(label="Image URL")
        heading = blocks.CharBlock()
        link_text = blocks.CharBlock()
        link_url = blocks.CharBlock()

    highlights = StreamField(
        [("highlight", HighlightItemBlock())],
        blank=True,
    )

    class TopicItemBlock(blocks.StructBlock):
        icon = blocks.CharBlock()
        text = blocks.CharBlock()
        url = blocks.CharBlock()

    topics = StreamField(
        [("topic", TopicItemBlock())],
        blank=True,
    )

    class BreakoutCardBlock(blocks.StructBlock):
        link_text = blocks.CharBlock()
        link_url = blocks.CharBlock()
        img_src = blocks.CharBlock(label="Image URL")

    breakout_cards = StreamField(
        [("card", BreakoutCardBlock())],
        blank=True,
    )

    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_heading", heading="Hero H1 (bold)"),
                FieldPanel(
                    "hero_heading_continued", heading="Hero H1 continued"
                ),
                FieldPanel("hero_image", heading="Image URL"),
            ],
            heading="Hero",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("highlights"),
            ],
            heading="Highlights",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("topics_heading"),
                FieldPanel("topics"),
            ],
            heading="Topics",
            classname="collapsible",
        ),
        # 5050 goes here
        MultiFieldPanel(
            [
                FieldPanel("breakout_cards_heading"),
                FieldPanel("breakout_cards"),
            ],
            heading="Breakout cards",
            classname="collapsible",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "v1/home_page/home_page.html"
