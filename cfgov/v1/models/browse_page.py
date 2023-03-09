from django.db import models

from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import StreamField

from data_research.blocks import MortgageDataDownloads
from jobmanager.blocks import JobListingTable
from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms, schema
from v1.models.base import CFGOVPage
from youth_employment.blocks import YESChecklist


class AbstractBrowsePage(CFGOVPage):
    navigation_label = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        help_text="Optional short label for left navigation.",
    )
    secondary_nav_exclude_sibling_pages = models.BooleanField(
        default=False,
        help_text="Don't show siblings of this page in the left navigation.",
    )

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        MultiFieldPanel(
            [
                FieldPanel("navigation_label"),
                FieldPanel(
                    "secondary_nav_exclude_sibling_pages",
                    heading="Exclude siblings",
                ),
            ],
            heading="Secondary navigation",
        ),
    ]

    class Meta:
        abstract = True

    def get_secondary_nav_items(self, request):
        nav_root = self

        # If the parent page of the current page is an AbstractBrowsePage,
        # we use it as the root page for the navigation sidebar.
        # Otherwise, we treat the current page as the navigation root.
        parent = self.get_parent().specific
        if isinstance(parent, AbstractBrowsePage):
            nav_root = parent

        # Should we show siblings of the navigation root page or not?
        if nav_root.secondary_nav_exclude_sibling_pages:
            pages = [nav_root]
        else:
            pages = (
                nav_root.get_siblings(inclusive=True)
                .type(AbstractBrowsePage)
                .live()
                .specific()
            )

        nav_items = []

        for page in pages:
            nav_item = self._make_nav_item(page, request)

            expanded = (page.pk == self.pk) or (page.pk == nav_root.pk)
            nav_item["expanded"] = expanded

            if expanded:
                children = (
                    page.get_children()
                    .type(AbstractBrowsePage)
                    .live()
                    .specific()
                )

                child_items = [
                    self._make_nav_item(child, request) for child in children
                ]
                if child_items:
                    nav_item["children"] = child_items

            nav_items.append(nav_item)

        return nav_items

    def _make_nav_item(self, page, request):
        active = self.pk == page.pk

        # Use self object to reflect draft/preview changes.
        if active:
            page = self

        return {
            "title": page.navigation_label or page.title,
            "url": page.get_url(request),
            "active": active,
        }


class BrowsePage(AbstractBrowsePage):
    header = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
            ("featured_content", organisms.FeaturedContent()),
            ("notification", molecules.Notification()),
        ],
        blank=True,
    )

    share_and_print = models.BooleanField(
        default=False,
        help_text="Include share and print buttons above page content.",
    )

    content = StreamField(
        [
            ("full_width_text", organisms.FullWidthText()),
            ("info_unit_group", organisms.InfoUnitGroup()),
            ("simple_chart", organisms.SimpleChart()),
            ("expandable_group", organisms.ExpandableGroup()),
            ("expandable", organisms.Expandable()),
            ("well", organisms.Well()),
            ("video_player", organisms.VideoPlayer()),
            ("snippet_list", organisms.ResourceList()),
            (
                "table_block",
                organisms.AtomicTableBlock(table_options={"renderer": "html"}),
            ),
            ("raw_html_block", blocks.RawHTMLBlock(label="Raw HTML block")),
            ("chart_block", organisms.ChartBlock()),
            ("mortgage_chart_block", organisms.MortgageChartBlock()),
            ("mortgage_map_block", organisms.MortgageMapBlock()),
            ("mortgage_downloads_block", MortgageDataDownloads()),
            ("data_snapshot", organisms.DataSnapshot()),
            ("job_listing_table", JobListingTable()),
            ("yes_checklist", YESChecklist()),
            ("raf_tool", v1_blocks.RAFTBlock()),
            ("faq_group", schema.FAQGroup()),
        ],
        blank=True,
    )

    # General content tab
    content_panels = AbstractBrowsePage.content_panels + [
        FieldPanel("header"),
        FieldPanel("share_and_print"),
        FieldPanel("content"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(AbstractBrowsePage.sidefoot_panels, heading="Sidebar"),
            ObjectList(
                AbstractBrowsePage.settings_panels, heading="Configuration"
            ),
        ]
    )

    template = "v1/browse-basic/index.html"

    page_description = "Left-hand navigation, no right-hand sidebar."
