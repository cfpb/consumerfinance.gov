from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.fields import StreamField

from data_research.blocks import MortgageDataDownloads
from jobmanager.blocks import JobListingTable
from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms, schema
from v1.models.base import CFGOVPage
from v1.util.util import get_secondary_nav_items
from youth_employment.blocks import YESChecklist


class BrowsePage(CFGOVPage):
    header = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
            ("featured_content", organisms.FeaturedContent()),
            ("notification", molecules.Notification()),
        ],
        blank=True,
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

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    share_and_print = models.BooleanField(
        default=False,
        help_text="Include share and print buttons above page content.",
    )

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("share_and_print"),
        FieldPanel("content"),
    ]

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel("secondary_nav_exclude_sibling_pages"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(sidefoot_panels, heading="Sidebar"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "v1/browse-basic/index.html"

    page_description = "Left-hand navigation, no right-hand sidebar."

    @property
    def page_js(self):
        return super().page_js + ["secondary-navigation.js"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update({"get_secondary_nav_items": get_secondary_nav_items})
        return context
