from wagtail.core import blocks

from v1.atomic_elements import organisms
from v1.atomic_elements.schema import FAQ, HowTo, Tip


class AskAnswerContent(blocks.StreamBlock):
    text = blocks.StructBlock(
        [
            (
                "anchor_tag",
                blocks.CharBlock(
                    required=False,
                    label="Anchor tag",
                    help_text="Add an optional anchor link tag to allow "
                    "linking directly to this block. Tag should "
                    "be unique and use dashes or underscores for "
                    "separation instead of spaces (ie, 'block-one-tag')",
                ),
            ),
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
            ),
        ]
    )
    table_block = organisms.AtomicTableBlock(
        table_options={"renderer": "html"}
    )
    tip = Tip()
    video_player = organisms.VideoPlayer()
    how_to_schema = HowTo()
    faq_schema = FAQ()

    class Meta:
        template = "v1/includes/blocks/schema/content-block.html"
