from wagtail.core import blocks

from v1.atomic_elements.organisms import AtomicTableBlock, VideoPlayer


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
    table_block = AtomicTableBlock(table_options={"renderer": "html"})
    tip = Tip()
    video_player = VideoPlayer()

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
