from time import time

from django.apps import apps
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.urls import resolve


# These messages are manually mirrored on the
# Javascript side in error-messages-config.js

ERROR_MESSAGES = {
    "CHECKBOX_ERRORS": {
        "required": 'Please select at least one of the "%s" options.'
    },
    "DATE_ERRORS": {
        "invalid": "You have entered an invalid date.",
    },
}


def get_unique_id(prefix="", suffix=""):
    index = hex(int(time() * 10000000))[2:]
    return prefix + str(index) + suffix


def valid_destination_for_request(request, url):
    view, args, kwargs = resolve(url)
    kwargs["request"] = request
    try:
        response = view(*args, **kwargs)
    except (Http404, TypeError):
        return False

    if isinstance(response, HttpResponseRedirect):
        # this indicates a permissions problem
        # (there may be a better way)
        if REDIRECT_FIELD_NAME + "=" in response.url:
            return False

    return True


def all_valid_destinations_for_request(request):
    possible_destinations = (
        ("Wagtail", "/admin/"),
        ("Django admin", "/django-admin/"),
    )
    valid_destinations = [
        pair
        for pair in possible_destinations
        if valid_destination_for_request(request, pair[1])
    ]

    return valid_destinations


def extended_strftime(dt, format):
    """
    Extend strftime with additional patterns:
    _m for custom month abbreviations,
    _d for day values without leading zeros.
    """
    _MONTH_ABBREVIATIONS = [
        None,
        "Jan.",
        "Feb.",
        "Mar.",
        "Apr.",
        "May",
        "Jun.",
        "Jul.",
        "Aug.",
        "Sept.",
        "Oct.",
        "Nov.",
        "Dec.",
    ]

    format = format.replace("%_d", dt.strftime("%d").lstrip("0"))
    format = format.replace("%_m", _MONTH_ABBREVIATIONS[dt.month])
    return dt.strftime(format)


def validate_social_sharing_image(image):
    """Raises a validation error if the image is too large or too small."""
    if image and (image.width > 4096 or image.height > 4096):
        raise ValidationError(
            "Social sharing image must be less than 4096w x 4096h"
        )


def get_page_from_path(path, root=None):
    """Given a string path, return the corresponding page object.

    If `root` is not passed, it is assumed you want to search from the root
    page of the default site.

    If `root` is passed, it will start the search from that page.

    If a page cannot be found at that path, returns `None`.
    """
    if root is None:
        site_model = apps.get_model("wagtailcore", "Site")
        site = site_model.objects.get(is_default_site=True)
        root = site.root_page

    path_components = [component for component in path.split("/") if component]

    try:
        route = root.route(None, path_components)
    except Http404:
        return None

    return route.page
