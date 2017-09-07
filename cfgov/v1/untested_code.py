from jinja2.ext import Extension

from v1.models import CFGOVRendition


def image_alt_value_dup(image):
    """Given an ImageBasic block or a CFGOVImage rendition as `image`,
    return the appropriate alt text.

    Return the CFGOVImage rendition's alt field, if present.
    Returns the alt field from the block, if it is set.
    Otherwise, returns the alt field from the CFGOVImage object, if it is set.
    Otherwise, returns an empty string.
    """

    # Check to see if the passed value is a CFGOVRendition
    if isinstance(image, CFGOVRendition):
        return image.alt

    # Otherwise, if it is a block
    if image:
        block_alt = image.get('alt')
        upload = image.get('upload')

        if block_alt:
            return block_alt
        elif upload and upload.alt:
            return upload.alt

    return ''


class V1ImagesExtensionDup(Extension):
    def __init__(self, environment):
        super(V1ImagesExtensionDup, self).__init__(environment)

        self.environment.globals.update({
            'image_alt_value_dup': image_alt_value_dup,
        })


# Nicer import names
images = V1ImagesExtensionDup
