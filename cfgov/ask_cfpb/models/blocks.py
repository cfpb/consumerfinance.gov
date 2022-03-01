from wagtail.core import blocks

from v1.atomic_elements import organisms


class Tip(blocks.StructBlock):
    content = blocks.RichTextBlock(features=["link", "document-link"], label="Tip")

    class Meta:
        icon = "title"
        template = "_includes/ask/tip.html"


class AskContent(blocks.StreamBlock):
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
    table_block = organisms.AtomicTableBlock(table_options={"renderer": "html"})
    tip = Tip()
    video_player = organisms.VideoPlayer()

    class Meta:
        template = "_includes/ask/content-block.html"


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
                ("step_content", AskContent()),
            ]
        )
    )

    class Meta:
        icon = "grip"
        template = "_includes/ask/how-to.html"
        label = "How To"


class FAQ(blocks.StructBlock):
    description = blocks.RichTextBlock(
        features=["ol", "ul", "bold", "italic", "link", "document-link"],
        blank=True,
        required=False,
    )
    questions = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("question", blocks.CharBlock(max_length=500)),
                ("answer_content", AskContent()),
            ]
        )
    )

    class Meta:
        icon = "grip"
        template = "_includes/ask/faq.html"
        label = "FAQ"


class AskAnswerContent(blocks.StreamBlock):
    text = blocks.StructBlock(
        [
            (
                "content",
                blocks.RichTextBlock(
                    features=[
                        "bold",
                        "italic",
                        "h2",
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
    table_block = organisms.AtomicTableBlock(table_options={"renderer": "html"})
    tip = Tip()
    video_player = organisms.VideoPlayer()
    how_to_schema = HowTo()
    faq_schema = FAQ()

    class Meta:
        template = "_includes/ask/content-block.html"
