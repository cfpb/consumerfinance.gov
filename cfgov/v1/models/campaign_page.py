from wagtail.admin.edit_handlers import (
    ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.core.blocks import StreamBlock, StructBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager
from wagtail.search import index

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.feeds import FilterableFeedPageMixin
from v1.models.base import CFGOVPage
from v1.util.filterable_list import FilterableListMixin


class CampaignHeader(StreamBlock):
    hero = molecules.Hero()
    features = organisms.InfoUnitGroup()

    class Meta:
        block_counts = {
            'hero': {'max_num': 1},
            'features': {'max_num': 1},
        }


class CampaignContent(StreamBlock):
    info_units = organisms.InfoUnitGroup()

    class Meta:
        block_counts = {
            'info_units': {'max_num': 2},
        }


class CampaignPage(CFGOVPage):
    header = StreamField(CampaignHeader, blank=True)
    content = StreamField(CampaignContent, blank=True)

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    # Sets page to only be createable as the child of the homepage
    parent_page_types = ['v1.HomePage']

    objects = PageManager()
