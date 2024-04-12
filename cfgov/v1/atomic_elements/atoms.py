from django.core.exceptions import ValidationError

from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.images.blocks import ImageChooserBlock


def is_required(field_name):
    return [str(field_name) + " is required."]


class Hyperlink(blocks.StructBlock):
    text = blocks.CharBlock(required=False)
    aria_label = blocks.CharBlock(
        required=False,
        help_text="Add an ARIA label if the link text does not describe the "
        "destination of the link (e.g. has ambiguous text like "
        '"Learn more" that is not descriptive on its own).',
    )
    url = blocks.CharBlock(default="/", required=False)
    is_link_boldface = blocks.BooleanBlock(default=False, required=False)

    def __init__(self, required=True):
        self.is_required = required
        super().__init__()

    @property
    def required(self):
        return self.is_required

    def clean(self, data):
        data = super().clean(data)

        if self.is_required and not data["text"]:
            raise StructBlockValidationError(
                block_errors={"text": ValidationError(is_required("Text"))}
            )

        return data

    class Meta:
        icon = "link"
        template = "v1/includes/atoms/hyperlink.html"


IMAGE_ALT_TEXT_HELP_TEXT = (
    "No character limit, but be as succinct as possible. If the image is "
    "decorative (i.e., a screenreader wouldn't have anything useful to say "
    "about it), leave this field blank."
)


class ImageBasicStructValue(blocks.StructValue):
    @property
    def url(self):
        if upload := self.get("upload"):
            return upload.get_rendition("original").url

    @property
    def alt_text(self):
        if alt := self.get("alt"):
            return alt
        elif upload := self.get("upload"):
            return upload.alt


class ImageBasic(blocks.StructBlock):
    upload = ImageChooserBlock(required=False)
    alt = blocks.CharBlock(required=False, help_text=IMAGE_ALT_TEXT_HELP_TEXT)

    def __init__(self, required=True):
        self.is_required = required
        super().__init__()

    @property
    def required(self):
        return self.is_required

    def clean(self, data):
        data = super().clean(data)

        if self.required and not data["upload"]:
            raise StructBlockValidationError(
                {"upload": ValidationError(is_required("Upload"))}
            )

        return data

    class Meta:
        icon = "image"
        value_class = ImageBasicStructValue
