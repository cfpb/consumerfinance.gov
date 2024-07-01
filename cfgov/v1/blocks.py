from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from wagtail import blocks
from wagtail.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock

from wagtail_footnotes.blocks import (
    FIND_FOOTNOTE_TAG,
)
from wagtail_footnotes.blocks import (
    RichTextBlockWithFootnotes as WagtailFootnotesRichTextBlockWithFootnotes,
)

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


class RichTextBlockWithFootnotes(WagtailFootnotesRichTextBlockWithFootnotes):
    def render_footnote_tag(self, index):
        template = get_template(settings.WAGTAIL_FOOTNOTES_REFERENCE_TEMPLATE)
        return template.render({"index": index})

    def replace_footnote_tags(self, value, html, context=None):
        # This is a wholesale copy of the replace_footnote_tags() method in
        # wagtail-footnotes's RichTextBlockWithFootnotes. It modifies the
        # embedded replace_tag() function to call our own
        # render_footnote_tag() method. This is a change that should be
        # contributed back upstream to allow straight-forward modification of
        # footnote link rendering.
        #
        # There is an alternative implementation proposed in a PR in 2022:
        #   https://github.com/torchbox/wagtail-footnotes/pull/27
        # But I think I prefer providing a new method to a new embedded func.
        if context is None:
            new_context = self.get_context(value)
        else:
            new_context = self.get_context(value, parent_context=dict(context))

        if not isinstance(new_context.get("page"), Page):
            return html

        page = new_context["page"]
        if not hasattr(page, "footnotes_list"):
            page.footnotes_list = []
        self.footnotes = {
            str(footnote.uuid): footnote for footnote in page.footnotes.all()
        }

        def replace_tag(match):
            try:
                index = self.process_footnote(match.group(1), page)
            except (KeyError, ValidationError):  # pragma: no cover
                return ""
            else:
                # This line is the only change to wagtail-footnote's
                # replace_footnote_tags(), providing a separate method that
                # can be overriden for rendering the footnote reference link.
                return self.render_footnote_tag(index)

        # note: we return safe html
        return mark_safe(FIND_FOOTNOTE_TAG.sub(replace_tag, html))  # noqa: S308
