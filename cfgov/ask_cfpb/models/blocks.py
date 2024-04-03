from wagtail import blocks

from v1.atomic_elements.organisms import Table, VideoPlayer
from v1.atomic_elements.schema import FAQ, HowTo


class Tip(blocks.StructBlock):
    content = blocks.RichTextBlock(
        features=["link", "document-link"], label="Tip"
    )

    class Meta:
        icon = "title"
        template = "ask-cfpb/tip.html"


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
    table = Table()
    tip = Tip(label="Tip (floats right)")
    video_player = VideoPlayer()
    how_to_schema = HowTo(label="Google Schema - How To")
    faq_schema = FAQ(label="Google Schema - FAQ")

    class Meta:
        template = "ask-cfpb/ask-answer-content.html"
