from jinja2 import contextfunction
from jinja2.ext import Extension

from v1.models import CFGOVRendition
from v1.templatetags.email_popup import email_popup
from v1.util.util import extended_strftime


def date_formatter(dt, text_format=False):
    format = '%_m %_d, %Y' if text_format else '%b %d, %Y'
    return extended_strftime(dt, format)


def image_alt_value(image):
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


def is_filter_selected(context, fieldname, value):
    request_get = context['request'].GET

    query_string_values = [
        k for k in
        request_get.getlist(fieldname) +
        request_get.getlist('filter_' + fieldname)
        if k
    ]

    return value in query_string_values


class V1FiltersExtension(Extension):
    def __init__(self, environment):
        super(V1FiltersExtension, self).__init__(environment)

        self.environment.globals.update({
            'date_formatter': date_formatter,
            'email_popup': email_popup,
            'image_alt_value': image_alt_value,
            'is_filter_selected': contextfunction(is_filter_selected),
        })


# Nicer import names
filters = V1FiltersExtension
