from __future__ import print_function, unicode_literals

import re

from functools import partial


HTTP_IMAGE_TAG_REGEX = r'<img[^>]*\ src=\\?\\?"(http://[^"]+)\\?\\?"'


def convert_http_image_links(html, url_mappings):
    """Convert HTTP image links according to a given set of URL mappings.

    url_mappings should be a list of tuples representing each pair of URL
    prefixes to convert from and to. For example:

        >> html = '<img src="http://from.url/path/image.png"/>'
        >> url_mappings = [('http://from.url/', 'http://to.url/')]
        >> convert_http_image_links(html, url_mappings)
        '<img src="http://to.url/path/image.png"/>'

    """
    converter = partial(
        convert_http_image_match,
        url_mappings=url_mappings
    )

    return re.sub(HTTP_IMAGE_TAG_REGEX, converter, html)


def convert_http_image_match(match, url_mappings):
    http_image_url = match.group(1)

    for from_prefix, to_prefix in url_mappings:
        if http_image_url.startswith(from_prefix):
            return re.sub(from_prefix, to_prefix, match.group(0))

    raise ValueError(
        'cannot convert HTTP image link {}'.format(http_image_url)
    )
