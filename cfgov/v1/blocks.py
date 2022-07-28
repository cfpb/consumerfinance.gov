from django.template.loader import render_to_string
from django.utils.safestring import SafeText, mark_safe
from django.utils.text import slugify

from wagtail.core import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from bs4 import BeautifulSoup

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
        template = "_includes/atoms/anchor-link.html"
        label = "Anchor link"


class HeadingIconBlock(blocks.CharBlock):
    classname = "heading-icon-block"
    form_classname = "heading-icon-block"


class HeadingLevelBlock(blocks.ChoiceBlock):
    choices = [
        ("h2", "H2"),
        ("h3", "H3"),
        ("h4", "H4"),
    ]
    classname = "heading-level-block"
    form_classname = "heading-level-block"


class HeadingTextBlock(blocks.CharBlock):
    classname = "heading-text-block"
    form_classname = "heading-text-block"


class HeadingBlock(blocks.StructBlock):
    text = HeadingTextBlock(required=False)
    level = HeadingLevelBlock(default="h2")
    icon = HeadingIconBlock(
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
        template = "_includes/blocks/heading.html"
        form_template = (
            "admin/form_templates/struct-with-block-wrapper-classes.html"
        )


class PlaceholderFieldBlock(blocks.FieldBlock):
    """
    Provides a render_form method that outputs a block
    placeholder, for use in a custom form_template.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = kwargs.pop("placeholder", None)

    def render_form(self, *args, **kwargs):
        # pragma: no cover
        prefix = ""
        value = "{}".format(*args)
        html = render_to_string(
            "wagtailadmin/block_forms/field.html",
            {
                "name": self.name,
                "classes": getattr(
                    self.meta, "form_classname", self.meta.classname
                ),
                "widget": self.field.widget.render(
                    prefix,
                    self.field.prepare_value(self.value_for_form(value)),
                    attrs={"id": format(prefix), "placeholder": self.label},
                ),
                "field": self.field,
                "errors": None,
            },
        )

        if self.placeholder is not None:
            html = self.replace_placeholder(html, self.placeholder)

        return html

    @staticmethod
    def replace_placeholder(html, placeholder):
        soup = BeautifulSoup(html, "html.parser")
        inputs = soup.findAll("input")

        if 1 != len(inputs):
            raise ValueError("block must contain a single input tag")

        inputs[0]["placeholder"] = placeholder

        return SafeText(soup)


class PlaceholderCharBlock(PlaceholderFieldBlock, blocks.CharBlock):
    class Meta:
        icon = "placeholder"
        form_template = (
            "admin/form_templates/struct_block_with_render_form.html"
        )


class ReusableTextChooserBlock(SnippetChooserBlock):
    class Meta:
        template = "_includes/snippets/reusable_text.html"


class RAFToolBlock(blocks.StaticBlock):
    class Meta:
        icon = "cog"
        label = "Rental Assistance Finder Tool"
        admin_text = "{label} has no options to configure".format(label=label)
        template = "_includes/blocks/raf_tool.html"

    class Media:
        js = ["erap.js"]


class RAFTBlock(blocks.StructBlock):
    county_threshold = blocks.IntegerBlock(
        required=False,
        help_text=(
            "Optional: Add a number to determine how many "
            "results trigger display of county dropdown "
            "for a state."
        ),
    )

    class Meta:
        icon = "cog"
        label = "RAF Tool (configurable)"
        template = "_includes/blocks/raf_tool.html"

    class Media:
        js = ["erap.js"]


class EmailSignUpChooserBlock(SnippetChooserBlock):
    def __init__(self, **kwargs):
        super().__init__("v1.EmailSignUp", **kwargs)

    class Meta:
        icon = "mail"
        template = "_includes/blocks/email-signup.html"

    class Media:
        js = ["email-signup.js"]
