from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField

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
        FieldPanel("header"),
        FieldPanel("content"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(CFGOVPage.sidefoot_panels, heading="Sidebar"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "v1/sublanding-page/index.html"

    page_description = (
        "Right-hand sidebar, no left-hand sidebar. Use if children should be "
        "searchable using standard search filters module."
    )


class ResearchHubPage(CategoryFilterableMixin, SublandingFilterablePage):
    template = "v1/sublanding-page/index.html"
    filterable_categories = ["Research Hub"]


class ActivityLogPage(CategoryFilterableMixin, SublandingFilterablePage):
    template = "v1/activity-log/index.html"
    filterable_categories = ("Blog", "Newsroom", "Research Report")
    filterable_per_page_limit = 100
