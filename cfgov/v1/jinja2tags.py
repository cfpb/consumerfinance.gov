from jinja2.ext import Extension


def image_alt_value(image):
    """Given an ImageBasic block as `image`, return the appropriate alt text.

    Returns the alt field from the block, if it is set.
    Otherwise, returns the alt field from the CFGOVImage object, if it is set.
    Otherwise, returns an empty string.
    """

    if image:
        block_alt = image.get('alt')
        upload = image.get('upload')

        if block_alt:
            return block_alt
        elif upload and upload.alt:
            return upload.alt

    return ''


class V1ImagesExtension(Extension):
    def __init__(self, environment):
        super(V1ImagesExtension, self).__init__(environment)

        self.environment.globals.update({
            'image_alt_value': image_alt_value,
        })


# Nicer import names
images = V1ImagesExtension
