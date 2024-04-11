from wagtail import blocks

from v1.atomic_elements.organisms import (
    FullWidthText,
    InfoUnitGroup,
    Table,
    VideoPlayer,
)


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
                        "h4",
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
    table = Table()
    video_player = VideoPlayer()

    class Meta:
        template = "v1/includes/blocks/schema/content-block.html"


class HowTo(blocks.StructBlock):
    title = blocks.CharBlock(max_length=500, label="Title of How To section")

    title_tag = blocks.ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        default="h2",
        help_text="Choose a tag for the title of the How To section.",
        label="Tag for How To section title",
    )

    show_title = blocks.BooleanBlock(
        default=True,
        required=False,
        help_text=(
            "The How To schema requires a title to let search engines "
            "understand what it is about. If you do not want the title to "
            "be displayed in the page, uncheck this box and the title "
            "content will only be made available to crawlers and "
            "screen readers."
        ),
        label="Show How To section title",
    )

    description = blocks.RichTextBlock(
        features=["ol", "ul", "bold", "italic", "link", "document-link"],
        blank=True,
        required=False,
    )

    step_title_tag = blocks.ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
            ("b", "Bold"),
            ("p", "Paragraph"),
        ],
        default="h3",
        help_text="Choose a tag for the title of each HowTo step.",
        label="Tag for step titles",
    )

    has_numbers = blocks.BooleanBlock(
        default=False,
        required=False,
        help_text=("Check this box to display numbers before step titles. "),
        label="Show numbers for steps",
    )

    steps = blocks.ListBlock(
        blocks.StructBlock(
            [
                (
                    "anchor_tag",
                    blocks.CharBlock(
                        max_length=500,
                        help_text=(
                            "Add an optional anchor link tag to allow "
                            "linking directly to this step. Tag should "
                            "be unique and use dashes or underscores "
                            "for separation instead of spaces "
                            "(ie, 'step-one-tag')."
                        ),
                        blank=True,
                        required=False,
                    ),
                ),
                (
                    "title",
                    blocks.CharBlock(
                        max_length=500,
                        help_text="Enter a title for this HowTo step. "
                        "You do not need to include a number in the title -- "
                        "numbers will be added automatically in the template "
                        "if the show numbers checkbox is checked.",
                    ),
                ),
                ("step_content", SchemaContent()),
            ]
        )
    )

    class Meta:
        icon = "grip"
        template = "v1/includes/blocks/schema/how-to.html"
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
                ("answer_content", SchemaContent()),
            ]
        )
    )

    class Meta:
        icon = "grip"
        template = "v1/includes/blocks/schema/faq.html"
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
                            ("full_width_text", FullWidthText()),
                            ("info_unit_group", InfoUnitGroup()),
                        ]
                    ),
                ),
            ]
        ),
        label="FAQ items",
    )

    class Meta:
        icon = "grip"
        template = "v1/includes/blocks/schema/faq-group.html"
        label = "FAQ"
