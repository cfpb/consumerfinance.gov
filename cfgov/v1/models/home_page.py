from django.db import models

from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.blocks import ListBlock, StructBlock, TextBlock

from v1.models.base import CFGOVPage


class home_card(StructBlock):
    icon = TextBlock()
    text = TextBlock()
    url = TextBlock()


class home_highlight(StructBlock):
    card_type = "highlight"
    img_src = TextBlock()
    heading = TextBlock()
    link_text = TextBlock()
    link_url = TextBlock()


class home_breakout(StructBlock):
    card_type = "breakout"
    link_text = TextBlock()
    link_url = TextBlock()
    img_src = TextBlock()


class HomeTopics(StructBlock):
    topics = ListBlock("home_card", default=list())


class HomeHighlights(StructBlock):
    highlights = ListBlock("home_highlight", default=list())


class HomeBreakouts(StructBlock):
    breakouts = ListBlock("home_breakout", default=list())


class HomePage(CFGOVPage):
    hero_heading = models.TextField(
        default="On your side",
        help_text=("Will be formatted in bold"),
    )

    hero_heading_continued = models.TextField(
        default="through life's financial moments."
    )

    hero_image = models.TextField()

    answers_heading = models.TextField(
        default="Find answers to your money questions",
    )

    breakout_cards_heading = models.TextField(
        default="Get help planning for future goals"
    )

    content_panels = CFGOVPage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_heading"),
                FieldPanel("hero_heading_continued"),
                FieldPanel("hero_image"),
            ],
            heading="Hero",
        ),
        FieldPanel("highlights"),
        MultiFieldPanel(
            [
                FieldPanel("answers_heading"),
                FieldPanel("home_topics", HomeTopics()),
            ],
            heading="Topics",
        ),
        # 50/50 goes here when we un-hardcode it
        MultiFieldPanel(
            [
                FieldPanel("breakout_cards_heading"),
                FieldPanel("breakout_cards"),
            ],
            heading="Breakout cards",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    def get_template(self, request, *args, **kwargs):
        try:
            return {
                "en": "v1/home_page/home_page.html",
                "es": "v1/home_page/home_page_legacy.html",
            }[self.language]
        except KeyError as e:
            raise NotImplementedError(
                f"Unsupported HomePage language: {self.language}"
            ) from e
