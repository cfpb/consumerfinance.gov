from wagtail.admin.panels import (
    FieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import StreamField

from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage


class HomePageb(CFGOVPage):
    hero = StreamField([("hero", molecules.JumboHero())])
    highlights = StreamField([("highlight", organisms.InfoUnitGroup())])
    topics = StreamField([("topic", organisms.CardBlockGroup())])
    callouts = StreamField([("callout", organisms.InfoUnitGroup())])
    breakouts = StreamField([("breakout", organisms.CardBlockGroup())])

    template = "v1/home_page/home_pageb.html"

    content_panels = CFGOVPage.content_panels + [
        FieldPanel("hero"),
        FieldPanel("highlights"),
        FieldPanel("topics"),
        FieldPanel("callouts"),
        FieldPanel("breakouts"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )
