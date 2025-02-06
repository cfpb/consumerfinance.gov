from wagtail.admin.panels import (
    FieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import StreamField

from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage


class HomePage(CFGOVPage):
    hero = StreamField([("hero", molecules.JumboHero())], blank=True)
    highlights = StreamField(
        [("highlight", organisms.InfoUnitGroup())], blank=True
    )
    topics = StreamField([("topic", organisms.CardBlockGroup())], blank=True)
    callouts = StreamField(
        [("callout", organisms.InfoUnitGroup())], blank=True
    )
    breakouts = StreamField(
        [("breakout", organisms.CardBlockGroup())], blank=True
    )

    template = "v1/home_page/home_page.html"

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
