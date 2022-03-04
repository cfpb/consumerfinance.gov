from wagtail.admin.edit_handlers import (
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager
from wagtail.search import index

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage


class LandingPage(CFGOVPage):
    header = StreamField(
        [
            ("hero", molecules.Hero()),
            ("text_introduction", molecules.TextIntroduction()),
        ],
        blank=True,
    )

    content = StreamField(
        [
            ("info_unit_group", organisms.InfoUnitGroup()),
            ("well", organisms.Well()),
            ("feedback", v1_blocks.Feedback()),
        ],
        blank=True,
    )

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("content"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.sidefoot_panels, heading="Sidebar"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "landing-page/index.html"

    objects = PageManager()

    search_fields = CFGOVPage.search_fields + [
        index.SearchField("content"),
        index.SearchField("header"),
    ]
