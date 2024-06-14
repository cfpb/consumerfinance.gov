from wagtail.images.jinja2tags import image as wagtail_image_fn
from wagtail.images.jinja2tags import images
from wagtail.images.models import AbstractImage

from v1.atomic_elements.atoms import ImageBasicStructValue
from v1.models.images import CFGOVImage, CFGOVRendition


def image_alt_value(image):
    """Return the appropriate alt text for an image object.

    If the image is a CFGOVRendition, return image.alt.
    If the image is a ImageBasicStructValue, return image.alt_text.
    If the image is a dict of attributes, return image.get("alt").

    As a fallback, return the empty string.
    """
    if isinstance(image, (CFGOVImage, CFGOVRendition)):
        return image.alt or ""
    elif isinstance(image, ImageBasicStructValue):
        return image.alt_text or ""
    elif isinstance(image, dict):
        return image.get("alt", "")

    return ""


def image_or_fallback(image, *args, **kwargs):
    if isinstance(image, AbstractImage):
        return wagtail_image_fn(image, *args, **kwargs)
    else:
        return image


class ImagesExtension(images):
    def __init__(self, environment):
        super().__init__(environment)
        self.environment.globals.update(
            {
                "image": image_or_fallback,
                "image_alt_value": image_alt_value,
            }
        )
