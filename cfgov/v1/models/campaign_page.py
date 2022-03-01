from wagtail.admin.edit_handlers import (
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager

from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage


class CampaignHeader(StreamBlock):
    hero = molecules.Hero()
    jumbo_hero = molecules.JumboHero()
    features = organisms.InfoUnitGroup()

    class Meta:
        block_counts = {
            "hero": {"max_num": 1},
            "jumbo_hero": {"max_num": 1},
            "features": {"max_num": 1},
        }


class CampaignContent(StreamBlock):
    info_units = organisms.InfoUnitGroup()

    class Meta:
        block_counts = {
            "info_units": {"max_num": 2},
        }


class CampaignPage(CFGOVPage):
    header = StreamField(CampaignHeader, blank=True)
    content = StreamField(CampaignContent, blank=True)

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("content"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    # Sets page to only be createable as the child of the homepage
    parent_page_types = ["v1.HomePage"]

    objects = PageManager()
