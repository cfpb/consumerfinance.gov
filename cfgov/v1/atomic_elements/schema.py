from wagtail.core import blocks

from v1.atomic_elements import organisms


class Tip(blocks.StructBlock):
    content = blocks.RichTextBlock(
        features=["link", "document-link"], label="Tip"
    )

    class Meta:
        icon = "title"
        template = "_includes/blocks/schema/tip.html"


class SchemaContent(blocks.StreamBlock):
    text = blocks.StructBlock(
        [
            (
                "content",
                blocks.RichTextBlock(
                    features=[
                        "bold",
                        "italic",
                        "h3",
                        "link",
                        "ol",
                        "ul",
                        "document-link",
                        "image",
                        "embed",
                    ],
                    label="Text",
                ),
            )
        ]
    )
    table_block = organisms.AtomicTableBlock(
        table_options={"renderer": "html"}
    )
    tip = Tip()
    video_player = organisms.VideoPlayer()

    class Meta:
        template = "_includes/blocks/schema/content-block.html"


class HowTo(blocks.StructBlock):
    title = blocks.CharBlock(max_length=500)

    description = blocks.RichTextBlock(
        features=["ol", "ul", "bold", "italic", "link", "document-link"],
        blank=True,
        required=False,
    )
    steps = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(max_length=500)),
                ("step_content", SchemaContent()),
            ]
        )
    )

    class Meta:
        icon = "grip"
        template = "_includes/blocks/schema/how-to.html"
        label = "How To"


class FAQ(blocks.StructBlock):
    """FAQ schema with limited content options for Ask CFPB"""

    description = blocks.RichTextBlock(
        features=["ol", "ul", "bold", "italic", "link", "document-link"],
        blank=True,
        required=False,
    )
    questions = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("question", blocks.CharBlock(max_length=500)),
                ("answer_content", SchemaContent()),
            ]
        )
    )

    class Meta:
        icon = "grip"
        template = "_includes/blocks/schema/faq.html"
        label = "FAQ"


class FAQGroup(blocks.StructBlock):
    has_top_rule_line = blocks.BooleanBlock(
        default=False,
        required=False,
        help_text=(
            "Check this to add a horizontal rule line to top of FAQ group."
        ),
    )
    lines_between_items = blocks.BooleanBlock(
        default=False,
        required=False,
        label="Show rule lines between items",
        help_text=(
            "Check this to show horizontal rule lines between FAQ items."
        ),
    )
    question_tag = blocks.ChoiceBlock(
        choices=[
            ("h2", "h2"),
            ("h3", "h3"),
            ("h4", "h4"),
            ("p", "p"),
        ],
        default="h2",
        help_text="HTML tag for questions.",
    )
    faq_items = blocks.ListBlock(
        blocks.StructBlock(
            [
                (
                    "anchor_tag",
                    blocks.CharBlock(
                        max_length=500,
                        help_text=(
                            "Add an optional anchor link tag for this "
                            "question. Tag should be unique and use "
                            "dashes or underscores for separation "
                            "instead of spaces (ie, 'question-one-tag')"
                        ),
                        blank=True,
                        required=False,
                    ),
                ),
                ("question", blocks.CharBlock(max_length=500)),
                (
                    "answer",
                    blocks.StreamBlock(
                        [
                            ("full_width_text", organisms.FullWidthText()),
                            ("info_unit_group", organisms.InfoUnitGroup()),
                        ]
                    ),
                ),
            ]
        ),
        label="FAQ items",
    )

    class Meta:
        icon = "grip"
        template = "_includes/blocks/schema/faq-group.html"
        label = "FAQ"
