from django.http import Http404, HttpResponse
from django.shortcuts import render

from flags.urls import flagged_re_path
from flags.views import FlaggedTemplateView
from wagtailsharing.views import ServeView


def flagged_wagtail_template_view(flag_name, template_name):
    """View that serves Wagtail if a flag is set, and a template if not.

    This uses the wagtail-sharing ServeView to ensure that sharing works
    properly when viewing the page in Wagtail behind a flag.
    """
    return FlaggedTemplateView.as_view(
        fallback=lambda request: ServeView.as_view()(request, request.path),
        flag_name=flag_name,
        template_name=template_name,
        condition=False,
    )


def flagged_wagtail_only_view(flag_name, regex_path, url_name=None):
    """If flag is set, serve page from Wagtail, otherwise raise 404."""

    def this_view_always_raises_http404(request, *args, **kwargs):
        raise Http404(f"flag {flag_name} not set")

    return flagged_re_path(
        flag_name,
        regex_path,
        lambda request: ServeView.as_view()(request, request.path),
        fallback=this_view_always_raises_http404,
        name=url_name,
    )


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
