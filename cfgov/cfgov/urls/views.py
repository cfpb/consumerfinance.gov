from django.http import HttpResponse
from django.shortcuts import render


def empty_200_response(request, *args, **kwargs):
    return HttpResponse(status=200)


def handle_error(code, request, exception=None):
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
