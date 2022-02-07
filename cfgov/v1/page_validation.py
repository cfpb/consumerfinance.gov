import re
from difflib import ndiff
from functools import partial

from wagtail.core.blocks import RawHTMLBlock

from v1.tests.wagtail_pages.helpers import save_page


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


class PageValidator:
    def __init__(self, http_image_url_mappings):
        self.http_image_url_mappings = http_image_url_mappings

    def validate_page(self, page, fix=False):
        diffsets = []

        for block in page.content:
            if not isinstance(block.block, RawHTMLBlock):
                continue

            try:
                corrected = self.correct_html(block.value)
            except Exception:
                print('failed page validation:', page.full_url)
                raise

            if corrected != block.value:
                diffset = ndiff(block.value.split('\n'), corrected.split('\n'))
                diffsets.append(
                    d for d in diffset
                    if d.startswith('- ') or d.startswith('+ ')
                )

                block.value = corrected

        if diffsets:
            print('\ndetected invalid page:', page.full_url)
            for diffset in diffsets:
                for diff in diffset:
                    print(diff)

            if fix:
                revision = save_page(page)

                if page.live:
                    revision.publish()

    def correct_html(self, html):
        return convert_http_image_links(html, self.http_image_url_mappings)
