from django.db import models

from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from jinja2 import pass_context

from jobmanager.blocks import JobListingList
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage
from v1.models.learn_page import AbstractFilterPage
from v1.serializers import FilterPageSerializer


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
            ("post_preview_snapshot", organisms.PostPreviewSnapshot()),
            ("contact", organisms.MainContactInfo()),
            ("table", organisms.Table()),
            ("expandable_group", organisms.ExpandableGroup()),
            ("expandable", organisms.Expandable()),
        ],
        blank=True,
    )
    sidebar_breakout = StreamField(
        [
            ("slug", blocks.CharBlock(icon="title")),
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
                            blocks.CharBlock(
                                help_text="Enter icon class name."
                            ),
                        ),
                        (
                            "heading",
                            blocks.CharBlock(
                                required=False, label="Introduction Heading"
                            ),
                        ),
                        (
                            "body",
                            blocks.TextBlock(
                                required=False, label="Introduction Body"
                            ),
                        ),
                    ],
                    heading="Breakout Image",
                    icon="image",
                ),
            ),
            ("job_listing_list", JobListingList()),
        ],
        blank=True,
    )

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        FieldPanel("header"),
        FieldPanel("content"),
        FieldPanel("portal_topic"),
        InlinePanel("footnotes", label="Footnotes"),
    ]

    sidebar_panels = [
        FieldPanel("sidebar_breakout"),
    ] + CFGOVPage.sidefoot_panels

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(sidebar_panels, heading="Sidebar"),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "v1/sublanding-page/index.html"

    @pass_context
    def get_browsefilterable_posts(self, context, limit):
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

        pages = sorted(
            posts_list, key=lambda p: p.date_published, reverse=True
        )[:limit]

        serializer = FilterPageSerializer(pages, many=True, context=context)
        return serializer.data

    @property
    def has_hero(self):
        """Returns boolean indicating whether the page includes a hero."""
        return bool(self.header.first_block_by_name("hero"))
