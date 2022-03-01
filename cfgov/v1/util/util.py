from time import time

from django.apps import apps
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.urls import resolve

from wagtail.core.blocks.stream_block import StreamValue
from wagtail.core.models import Site


# These messages are manually mirrored on the
# Javascript side in error-messages-config.js

ERROR_MESSAGES = {
    "CHECKBOX_ERRORS": {"required": 'Please select at least one of the "%s" options.'},
    "DATE_ERRORS": {
        "invalid": "You have entered an invalid date.",
    },
}


def get_unique_id(prefix="", suffix=""):
    index = hex(int(time() * 10000000))[2:]
    return prefix + str(index) + suffix


def instanceOfBrowseOrFilterablePages(page):
    from ..models import BrowseFilterablePage, BrowsePage

    pages = (BrowsePage, BrowseFilterablePage)
    return isinstance(page, pages)


# For use by Browse type pages to get the secondary navigation items
# TODO: Move into BrowsePage class once BrowseFilterablePage has been merged
# into BrowsePage
def get_secondary_nav_items(request, current_page):
    # If the parent page of the current page is a BrowsePage or a
    # BrowseFilterablePage, then use that as the top-level page for the
    # purposes of the navigation sidebar. Otherwise, treat the current page
    # as top-level.
    parent = current_page.get_parent().specific
    if instanceOfBrowseOrFilterablePages(parent):
        page = parent
    else:
        page = current_page

    # If there's no appropriate page version (e.g. not published for a sharing
    # request), then return no sidebar at all.
    if not page:
        return [], False

    # Return a boolean about whether or not the current page has Browse
    # children
    has_children = False

    if page.secondary_nav_exclude_sibling_pages:
        pages = [page]
    else:
        pages = filter(
            lambda p: instanceOfBrowseOrFilterablePages(p.specific),
            page.get_appropriate_siblings(),
        )

    site = Site.find_for_request(request)

    nav_items = []
    for sibling in pages:
        if page.id == sibling.id:
            sibling = page
        else:
            sibling = sibling

        item_selected = current_page.pk == sibling.pk

        item = {
            "title": sibling.title,
            "slug": sibling.slug,
            "url": sibling.relative_url(site),
            "children": [],
            "active": item_selected,
            "expanded": item_selected,
        }

        if page.id == sibling.id:
            visible_children = list(
                filter(
                    lambda c: (instanceOfBrowseOrFilterablePages(c) and (c.live)),
                    sibling.get_children().specific(),
                )
            )
            if len(visible_children):
                has_children = True
                for child in visible_children:
                    child_selected = current_page.pk == child.pk

                    if child_selected:
                        item["expanded"] = True

                    item["children"].append(
                        {
                            "title": child.title,
                            "slug": child.slug,
                            "url": child.relative_url(site),
                            "active": child_selected,
                        }
                    )

        nav_items.append(item)

    # Add `/process/` segment to BAH journey page nav urls.
    # TODO: Remove this when redirects for `/process/` urls
    # are added after 2018 homebuying campaign.
    journey_urls = (
        "/owning-a-home/prepare",
        "/owning-a-home/explore",
        "/owning-a-home/compare",
        "/owning-a-home/close",
        "/owning-a-home/sources",
    )
    if current_page.relative_url(site).startswith(journey_urls):
        for item in nav_items:
            item["url"] = item["url"].replace("owning-a-home", "owning-a-home/process")
            for child in item["children"]:
                child["url"] = child["url"].replace(
                    "owning-a-home", "owning-a-home/process"
                )
    # END TODO

    return nav_items, has_children


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


def get_streamfields(page):
    """
    Retrieves the stream values on a page from its Streamfield
    """
    blocks_dict = {}
    for key, value in vars(page).items():
        if isinstance(value, StreamValue):
            blocks_dict.update({key: value})
    return blocks_dict


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
        raise ValidationError("Social sharing image must be less than 4096w x 4096h")


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
