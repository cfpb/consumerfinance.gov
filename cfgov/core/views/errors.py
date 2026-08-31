from http import HTTPStatus
from urllib.parse import quote

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.cache import patch_vary_headers


HTML = "text/html"
JSON = "application/json"
# https://www.rfc-editor.org/rfc/rfc9457
PROBLEM_JSON = "application/problem+json"
TEXT = "text/plain"

# Clients sending "Accept: */*" get the first entry in this list.
# Default to full HTML page, but also support simpler responses when possible.
ERROR_RESPONSE_TYPES = [HTML, JSON, PROBLEM_JSON, TEXT]


def _is_simple_404_path(path):
    """Is this a request that nobody is ever going to look at?

    Return a simple 404 response for certain URL paths that aren't being
    viewed in a browser by a human.
    """
    prefixes = [
        # Well-known URIs: https://www.rfc-editor.org/rfc/rfc8615
        "/.well-known/",
        # Static files
        settings.STATIC_URL,
    ]

    return path.startswith(tuple(prefixes))


def _problem_json_error(code, request):
    """An RFC 9457 problem details response.

    https://www.rfc-editor.org/rfc/rfc9457
    """
    return JsonResponse(
        {
            "type": "about:blank",
            "title": HTTPStatus(code).phrase,
            "status": code,
            "instance": quote(request.path),
        },
        status=code,
        content_type=PROBLEM_JSON,
    )


def _text_error(code):
    return HttpResponse(
        f"{code} {HTTPStatus(code).phrase}\n".encode(),
        status=code,
        content_type="text/plain; charset=utf-8",
    )


def _html_error(code, request):
    try:
        return render(
            request,
            f"v1/layouts/{code}.html",
            context={"request": request},
            status=code,
        )
    except Exception:
        # If we encounter an exception when rendering a 500 error page, we
        # want to handle it so that we don't trigger infinite recursion
        # (error -> try rendering error page -> another error -> etc).
        # In that case, we fall back to a plain text error HTTP response.
        #
        # For other errors (like 404s), we do want to raise the exception,
        # so that we (hopefully correctly) log and render the 500 page.
        if code != 500:
            raise

        return HttpResponse(
            f"This request could not be processed, HTTP Error {str(code)}.",
            status=code,
        )


def handle_error(code, request, exception=None):
    # Return empty text/plain 404 for certain URLs.
    if code == 404 and _is_simple_404_path(request.path):
        return HttpResponse(
            status=404, content_type="text/plain; charset=utf-8"
        )

    # Return a different response type for different Accept: headers.
    media_type = request.get_preferred_type(ERROR_RESPONSE_TYPES)

    if media_type in (JSON, PROBLEM_JSON):
        response = _problem_json_error(code, request)
    elif media_type == HTML:
        response = _html_error(code, request)
    else:
        # Either the client asked for text/plain, or it accepts nothing we
        # can produce. Plain text is the safest thing to send.
        response = _text_error(code)

    # Make sure anything that might be caching this response knows to vary its
    # cache by the Accept header.
    patch_vary_headers(response, ("Accept",))

    return response
