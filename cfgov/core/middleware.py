import re

from django.conf import settings
from django.utils.encoding import force_text

try:
    from wagtail.core.rich_text import expand_db_html
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailcore.rich_text import expand_db_html

from core.utils import add_link_markup, get_link_tags


class DownstreamCacheControlMiddleware(object):
    def process_response(self, request, response):
        if 'CSRF_COOKIE_USED' in request.META:
            response['Edge-Control'] = 'no-store'
        return response


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

    link_tags = get_link_tags(expanded_html)
    for tag in link_tags:
        tag_with_markup = add_link_markup(tag)
        if tag_with_markup:
            expanded_html = expanded_html.replace(
                tag,
                tag_with_markup
            )

    return expanded_html


class ParseLinksMiddleware(object):
    def process_response(self, request, response):
        if self.should_parse_links(request.path, response['content-type']):
            response.content = parse_links(
                response.content,
                encoding=response.charset
            )
        return response

    @classmethod
    def should_parse_links(cls, request_path, response_content_type):
        """Determine if links should be parsed for a given request/response.

        Returns True if

        1. The response has the default content type (HTML) AND
        2. The request path does not match settings.PARSE_LINKS_EXCLUSION_LIST

        Otherwise returns False.
        """
        if settings.DEFAULT_CONTENT_TYPE not in response_content_type:
            return False

        return not any(
            re.search(regex, request_path)
            for regex in settings.PARSE_LINKS_EXCLUSION_LIST
        )
