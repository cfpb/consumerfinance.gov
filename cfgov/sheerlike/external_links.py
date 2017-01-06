import warnings

from django.conf import settings

from v1 import parse_links
from v1.page_validation import convert_http_image_links
from v1.s3utils import http_s3_url_prefix, https_s3_url_prefix


def process_external_link_field(field):
    # Convert any HTTP image links to S3 to HTTPS.
    # noop if AWS_STORAGE_BUCKET_NAME is not set
    if getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None):
        field = convert_http_image_links(field, [
            (http_s3_url_prefix(), https_s3_url_prefix()),
        ])

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
