import re

from django.conf import settings
from django.utils import translation
from django.utils.encoding import force_str

from wagtail.core.rich_text import expand_db_html

from core.utils import add_link_markup, get_body_html, get_link_tags


class DownstreamCacheControlMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 'CSRF_COOKIE_USED' in request.META:
            response['Edge-Control'] = 'no-store'
        return response


def parse_links(html, request_path=None, encoding=None):
    """Process all links in given html and replace them if markup is added."""
    if encoding is None:
        encoding = settings.DEFAULT_CHARSET

    # The passed HTML may be a string or bytes, depending on what is calling
    # this method. For example, Django response.content is always bytes. We
    # always want this content to be a string for our purposes.
    html_as_text = force_str(html, encoding=encoding)

    # This call invokes Wagtail-specific logic that converts references to
    # Wagtail pages, documents, and images to their proper link URLs.
    expanded_html = expand_db_html(html_as_text)

    # Parse links only in the <body> of the HTML
    body_html = get_body_html(expanded_html)
    if body_html is None:
        return expanded_html

    link_tags = get_link_tags(body_html)
    for tag in link_tags:
        tag_with_markup = add_link_markup(tag, request_path)
        if tag_with_markup:
            expanded_html = expanded_html.replace(
                tag,
                tag_with_markup
            )

    return expanded_html


class ParseLinksMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
<<<<<<< HEAD
        if self.should_parse_links(
            request.path,
            response.get('Content-Type', '')
        ):
=======
        if 'content-type' in response and self.should_parse_links(request.path, response['content-type']):
>>>>>>> dev setup
            response.content = parse_links(
                response.content,
                request.path,
                encoding=response.charset
            )
        return response



    @classmethod
    def should_parse_links(cls, request_path, response_content_type):
        """Determine if links should be parsed for a given request/response.

        Returns True if

        1. The response has the settings.DEFAULT_CONTENT_TYPE (HTML) AND
        2. The request path does not match settings.PARSE_LINKS_EXCLUSION_LIST

        Otherwise returns False.
        """
        if "html" not in response_content_type:
            return False

        return not any(
            re.search(regex, request_path)
            for regex in settings.PARSE_LINKS_EXCLUSION_LIST
        )


class DeactivateTranslationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        translation.deactivate()
        return response
