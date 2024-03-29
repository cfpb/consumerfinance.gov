import html
import re

from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from v1.util.util import get_unique_id


class AnchorLink(blocks.StructBlock):
    link_id = blocks.CharBlock(
        required=False,
        label="ID for this content block",
        help_text="""
            ID will be auto-generated on save.
            However, you may enter some human-friendly text that
            will be incorporated to make it easier to read.
        """,
    )

    def clean(self, data):
        def format_id(string):
            if string == "anchor":
                return get_unique_id("anchor_")
            elif "anchor" in string:
                return slugify(string)
            else:
                suffix = "_" if string else ""
                return get_unique_id("anchor_" + slugify(string) + suffix)

        data["link_id"] = format_id(data["link_id"])
        data = super().clean(data)
        return data

    class Meta:
        icon = "link"
        template = "v1/includes/atoms/anchor-link.html"
        label = "Anchor link"


class HeadingBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=False)
    level = blocks.ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
            ("h5", "H5"),
        ],
        default="h2",
    )
    icon = blocks.CharBlock(
        required=False,
        help_text=mark_safe(
            "Input the name of an icon to appear to the left of the heading. "
            "E.g., approved, help-round, etc. "
            '<a href="https://cfpb.github.io/design-system/'
            'foundation/iconography">See full list of icons</a>'
        ),
    )

    class Meta:
        icon = "title"
        template = "v1/includes/blocks/heading.html"
        form_classname = "struct-block heading-block"


class ReusableTextChooserBlock(SnippetChooserBlock):
    class Meta:
        template = "v1/includes/snippets/reusable_text.html"


class ReusableNotificationChooserBlock(SnippetChooserBlock):
    class Meta:
        template = "v1/includes/snippets/reusable_notification.html"


class EmailSignUpChooserBlock(SnippetChooserBlock):
    def __init__(self, **kwargs):
        super().__init__("v1.EmailSignUp", **kwargs)

    class Meta:
        icon = "mail"
        template = "v1/includes/blocks/email-signup.html"

    class Media:
        js = ["email-signup.js"]


class EscapedHTMLValidator:
    """
    Implicity used on all UnescapedRichTextBlocks to limit "raw" HTML elements
    """

    def __init__(self, allowed_elements=()):
        # Regular expression to match a user-entered HTML tag, which shows up
        # in the rich text value with HTML entities around the tag name and
        # attributes (i.e. &lt;span id="foo"&gt;).
        self.escaped_html_re = re.compile(
            r"&lt;(?P<tag_name>\w+)(?:(?!&gt;).)*?&gt;"
        )
        self.allowed_elements = allowed_elements

    def __call__(self, value):
        element_matches = self.escaped_html_re.findall(str(value))
        invalid_elements = [
            tag_name
            for tag_name in element_matches
            if tag_name not in self.allowed_elements
        ]
        if len(invalid_elements) > 0:
            raise ValidationError(
                "Invalid HTML element(s) found: "
                f"{', '.join(invalid_elements)}. "
                "The only HTML elements allowed are "
                f"{', '.join(self.allowed_elements)}. "
            )


class UnescapedRichTextBlock(blocks.RichTextBlock):
    """
    Unescape any HTML entities within the rich text block to allow raw HTML.

    THIS BLOCK EXISTS TEMPORARILY UNTIL EXISTING RAW HTML USAGE IS REMOVED.
    DO NOT ADD THIS BLOCK TO ANY NEW FIELDS.
    """

    def __init__(self, validators=(), **kwargs):
        validators = list(validators) + [
            EscapedHTMLValidator(
                allowed_elements=(
                    "svg",
                    "path",
                )
            )
        ]

        super().__init__(validators=validators, **kwargs)

    def to_python(self, value):
        value = html.unescape(value)
        return super().to_python(value)
