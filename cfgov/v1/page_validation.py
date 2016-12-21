from __future__ import print_function, unicode_literals

import re

from django.conf import settings
from functools import partial

from v1.s3utils import https_s3_url_prefix


HTTP_IMAGE_TAG_REGEX = r'<img[^>]*\ src=\\?\\?"(http://[^"]+)\\?\\?"'


def convert_http_image_match(match, convert_url_prefixes):
    """Convert an HTTP link matching a URL prefix to an HTTPS link to S3."""
    http_image_url = match.group(1)
    https_prefix = https_s3_url_prefix()

    for url_prefix in convert_url_prefixes:
        if http_image_url.startswith(url_prefix):
            print('altering link {} to start with {} instead of {}'.format(
                match.group(0),
                https_prefix,
                url_prefix
            ))
            return re.sub(url_prefix, https_prefix, match.group(0))

    raise ValueError(
        'cannot convert HTTP image link {}'.format(http_image_url)
    )


def convert_http_image_links(html, convert_url_prefixes):
    """Convert HTTP image links matching given URL prefixes to MEDIA_URL."""
    converter = partial(
        convert_http_image_match,
        convert_url_prefixes=convert_url_prefixes
    )

    return re.sub(HTTP_IMAGE_TAG_REGEX, converter, html)
