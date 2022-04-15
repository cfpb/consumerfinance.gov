from wagtail.admin.edit_handlers import (
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.search import index

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage
from v1.models.filterable_list_mixins import (
    CategoryFilterableMixin,
    FilterableListMixin,
)


class SublandingFilterableContent(StreamBlock):
    """Defines the StreamField blocks for SublandingFilterablePage content.

    Pages can have at most one filterable list.
    """

    text_introduction = molecules.TextIntroduction()
    full_width_text = organisms.FullWidthText()
    filter_controls = organisms.FilterableList()
    featured_content = organisms.FeaturedContent()
    feedback = v1_blocks.Feedback()

    class Meta:
        block_counts = {
            "filter_controls": {"max_num": 1},
        }


class SublandingFilterablePage(FilterableListMixin, CFGOVPage):
    header = StreamField(
        [
            ("hero", molecules.Hero()),
        ],
        blank=True,
    )
    content = StreamField(SublandingFilterableContent)

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

    template = "sublanding-page/index.html"

    search_fields = CFGOVPage.search_fields + [
        index.SearchField("content"),
        index.SearchField("header"),
    ]


class ActivityLogPage(CategoryFilterableMixin, SublandingFilterablePage):
    template = "activity-log/index.html"
    filterable_categories = ("Blog", "Newsroom", "Research Report")
    filterable_per_page_limit = 100
