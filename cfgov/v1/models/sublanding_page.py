from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

from jobmanager.blocks import JobListingList
from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage
from v1.models.learn_page import AbstractFilterPage


class SublandingPage(CFGOVPage):
    portal_topic = models.ForeignKey(
        "v1.PortalTopic",
        blank=True,
        null=True,
        related_name="portal_pages",
        on_delete=models.SET_NULL,
        help_text="Select a topic if this is a MONEY TOPICS portal page.",
    )
    header = StreamField(
        [
            ("hero", molecules.Hero()),
        ],
        blank=True,
    )
    content = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
            ("notification", molecules.Notification()),
            ("featured_content", organisms.FeaturedContent()),
            ("full_width_text", organisms.FullWidthText()),
            ("info_unit_group", organisms.InfoUnitGroup()),
            ("well", organisms.Well()),
            ("snippet_list", organisms.ResourceList()),
            ("post_preview_snapshot", organisms.PostPreviewSnapshot()),
            ("contact", organisms.MainContactInfo()),
            (
                "table_block",
                organisms.AtomicTableBlock(table_options={"renderer": "html"}),
            ),
            ("reg_comment", organisms.RegComment()),
            ("feedback", v1_blocks.Feedback()),
        ],
        blank=True,
    )
    sidebar_breakout = StreamField(
        [
            ("slug", blocks.CharBlock(icon="title")),
            ("heading", blocks.CharBlock(icon="title")),
            ("paragraph", blocks.RichTextBlock(icon="edit")),
            (
                "breakout_image",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock()),
                        (
                            "is_round",
                            blocks.BooleanBlock(
                                required=False, default=True, label="Round?"
                            ),
                        ),
                        (
                            "icon",
                            blocks.CharBlock(help_text="Enter icon class name."),
                        ),
                        (
                            "heading",
                            blocks.CharBlock(
                                required=False, label="Introduction Heading"
                            ),
                        ),
                        (
                            "body",
                            blocks.TextBlock(required=False, label="Introduction Body"),
                        ),
                    ],
                    heading="Breakout Image",
                    icon="image",
                ),
            ),
            ("related_posts", organisms.RelatedPosts()),
            ("job_listing_list", JobListingList()),
        ],
        blank=True,
    )

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("content"),
        FieldPanel("portal_topic"),
    ]

    sidebar_panels = [
        StreamFieldPanel("sidebar_breakout"),
    ] + CFGOVPage.sidefoot_panels

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(sidebar_panels, heading="Sidebar"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "sublanding-page/index.html"

    objects = PageManager()

    search_fields = CFGOVPage.search_fields + [
        index.SearchField("content"),
        index.SearchField("header"),
    ]

    def get_browsefilterable_posts(self, limit):
        filter_pages = [
            p.specific
            for p in self.get_appropriate_descendants()
            if "FilterablePage" in p.specific_class.__name__
            and "archive" not in p.title.lower()
        ]
        posts_list = []
        for page in filter_pages:
            posts_list.extend(
                AbstractFilterPage.objects.live().filter(
                    CFGOVPage.objects.child_of_q(page)
                )
            )

        return sorted(posts_list, key=lambda p: p.date_published, reverse=True)[:limit]
