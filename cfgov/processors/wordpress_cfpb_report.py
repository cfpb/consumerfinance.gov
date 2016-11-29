import json
import os.path
import re
import requests
import sys

from sheerlike.external_links import process_external_links
from sheerlike.helpers import process_string_fields


def posts_at_url(url):
    current_page = 1
    max_page = sys.maxint

    while current_page <= max_page:
        url = os.path.expandvars(url)
        resp = requests.get(url, params={'page': current_page, 'count': '-1'})
        results = json.loads(resp.content)
        current_page += 1
        max_page = results['pages']

        for p in results['posts']:
            yield p


def documents(name='', url='', **kwargs):
    for post in posts_at_url(url):
        yield process_post(post)


HTTP_IMAGE_TAG_REGEX = r'<img[^>]*\ src=\\?\\?"http://([^"]+)\\?\\?"'


def convert_http_image_link(field):
    match = re.search(HTTP_IMAGE_TAG_REGEX, field)

    if match:
        print(field)
        print(match.group(1))


def process_post(page):
    del page['comments']
    page['_id'] = page['id']

    page = process_external_links(page)
    page = process_string_fields(page, callback=convert_http_image_link)

    return {'_type': 'report',
            '_id': page['id'],
            '_source': page}
