from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

from wagtail import blocks
from wagtail.images import blocks as images_blocks

from v1.blocks import HeadingBlock


class ImageMapCoordinates(blocks.StructBlock):
    left = blocks.FloatBlock(
        required=True,
        min_value=0,
        max_value=100,
        label="X value (in percentage)",
    )
    top = blocks.FloatBlock(
        required=True,
        min_value=0,
        max_value=100,
        label="Y value (in percentage)",
    )
    width = blocks.FloatBlock(
        required=True,
        min_value=0,
        max_value=100,
        label="Width (in percentage)",
    )
    height = blocks.FloatBlock(
        required=True,
        min_value=0,
        max_value=100,
        label="Height (in percentage)",
    )

    def clean(self, value):
        cleaned = super().clean(value)
        errors = {}
        if cleaned.get("left") + cleaned.get("width") > 100:
            errors["left"] = errors["width"] = ErrorList(
                ["Sum of left and width values should not exceed 100."]
            )
        if cleaned.get("top") + cleaned.get("height") > 100:
            errors["top"] = errors["height"] = ErrorList(
                ["Sum of top and height values should not exceed 100."]
            )
        if errors:
            raise ValidationError(
                "Validation error in ImageMapCoordinates", params=errors
            )
        return cleaned


class ExplainerNote(blocks.StructBlock):
    heading = blocks.CharBlock(required=True, label="Expandable header")
    body = blocks.RichTextBlock(
        required=True,
        features=["bold", "italic", "link", "document-link"],
        label="Expandable text",
    )
    coordinates = ImageMapCoordinates(
        label="Image coordinates",
        help_text=mark_safe(
            "Enter percentage values for the highlighted "
            "area of the image associated with this expandable. See "
            '<a href="https://github.cfpb.gov/CFPB/hubcap/wiki/Form-'
            'explainer-page#add-image-coordinates">Hubcap documentation</a> '
            "for more information on identifying coordinates."
        ),
    )


class ExplainerCategory(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        label="Category title",
        help_text="Optional. Leave blank if there is only "
        "one type of note for this image.",
    )
    notes = blocks.ListBlock(
        ExplainerNote(required=False),
        default=[],
    )


class ExplainerPage(blocks.StructBlock):
    image = images_blocks.ImageChooserBlock(required=True, icon="image")
    categories = blocks.ListBlock(ExplainerCategory(required=False))


class Explainer(blocks.StructBlock):
    heading = HeadingBlock(required=False, label="Heading (optional)")

    pages = blocks.ListBlock(ExplainerPage(required=False))

    class Meta:
        template = "form-explainer/blocks/explainer.html"
        icon = "doc-full-inverse"
        label = "Explainer"
