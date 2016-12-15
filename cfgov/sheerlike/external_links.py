import re
import warnings

from django.conf import settings

from v1 import parse_links


HTTP_IMAGE_TAG_REGEX = r'<img[^>]*\ src=\\?\\?"(http://[^"]+)\\?\\?"'


def convert_http_image_match(match):
    http_image_url = match.group(1)

    s3_url = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
    if not s3_url:
        raise RuntimeError(
            'cannot convert HTTP image links without defined s3 bucket'
        )

    if not http_image_url.startswith('http://' + s3_url):
        raise ValueError(
            'cannot convert HTTP image link {}'.format(http_image_url)
        )

    return re.sub(
        'http://' + s3_url,
        'https://' + s3_url + '.s3.amazonaws.com',
        match.group(0)
    )


def convert_http_image_links(field):
    return re.sub(HTTP_IMAGE_TAG_REGEX, convert_http_image_match, field)


def process_external_link_field(field):
    # Convert any HTTP image links to S3 to HTTPS.
    field = convert_http_image_links(field)

    # Add appropriate markup to all links in HTML.
    field = parse_links(field).encode(formatter=None)

    return field


def process_external_links(doc):
    warnings.filterwarnings('ignore')
    doc = _process_data(doc)
    warnings.resetwarnings()
    return doc


def _process_data(field):
    if isinstance(field, basestring):
        field = process_external_link_field(field)
    elif isinstance(field, list):
        for i, value in enumerate(field):
            field[i] = _process_data(value)
    elif isinstance(field, dict):
        for key, value in field.iteritems():
            field[key] = _process_data(value)
    return field
