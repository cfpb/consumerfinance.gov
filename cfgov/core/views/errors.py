from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


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

    # Otherwise return the full HTML error page.
    return _html_error(code, request)
