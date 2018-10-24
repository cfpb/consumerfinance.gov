from six import text_type as str

from django.conf import settings
from django.utils.encoding import force_text

from wagtail.wagtailcore.rich_text import expand_db_html

from bs4 import BeautifulSoup

from core.utils import add_link_markup, get_link_tags


class DownstreamCacheControlMiddleware(object):
    def process_response(self, request, response):
        if 'CSRF_COOKIE_USED' in request.META:
            response['Edge-Control'] = 'no-store'
        return response


def should_parse_links(request_path, content_type):
    """ Do not parse links for paths in the blacklist,
    or for content that is not html
    """
    for path in settings.PARSE_LINKS_BLACKLIST:
        if request_path.startswith(path):
            return False

    if settings.DEFAULT_CONTENT_TYPE not in content_type:
        return False

    return True


def parse_links(html, encoding=None):
    """Process all links in given html and replace them if markup is added."""
    if encoding is None:
        encoding = settings.DEFAULT_CHARSET

    # The passed HTML may be a string or bytes, depending on what is calling
    # this method. For example, Django response.content is always bytes. We
    # always want this content to be a string for our purposes.
    html_as_text = force_text(html, encoding=encoding)

    # This call invokes Wagail-specific logic that converts references to
    # Wagtail pages, documents, and images to their proper link URLs.
    expanded_html = expand_db_html(html_as_text)

    soup = BeautifulSoup(expanded_html, 'html.parser')
    link_tags = get_link_tags(soup)
    for tag in link_tags:
        original_link = str(tag)
        link_with_markup = add_link_markup(tag)
        if link_with_markup:
            expanded_html = expanded_html.replace(
                original_link,
                link_with_markup
            )

    return expanded_html


class ParseLinksMiddleware(object):
    def process_response(self, request, response):
        if should_parse_links(request.path, response['content-type']):
            response.content = parse_links(
                response.content,
                encoding=response.charset
            )
        return response
