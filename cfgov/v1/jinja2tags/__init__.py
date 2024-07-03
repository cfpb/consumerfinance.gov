from jinja2 import pass_context
from jinja2.ext import Extension

from core.feature_flags import environment_is
from v1.templatetags.app_urls import app_page_url, app_url
from v1.util import ref
from v1.util.util import get_unique_id

from .datetimes import DatetimesExtension
from .images import ImagesExtension


def is_filter_selected(context, fieldname, value):
    """Check URL query parameters to see if a filter option should be selected

    Returns True if fieldname=value is found in the GET data in order to output
    the `checked` attribute on a checkbox or radio button in the
    _render_filter_fields macro (see: filterable-list-controls.html).
    """
    request_get = context["request"].GET

    return value and value in request_get.getlist(fieldname)


def unique_id_in_context(context):
    """Return an ID that is unique within the given context

    For a given request, return a unique ID each time this method is
    called. The goal is to generate IDs to uniquely identify elements
    in a template that are consistent between page loads.

    If the context has a request object, the generated id will increment:

    >>> context = {'request': request}
    >>> unique_id_in_context(context)  # returns 1
    >>> unique_id_in_context(context)  # returns 2
    >>> unique_id_in_context(context)  # returns 3

    If the context lacks a request, this function will return a 14-character
    unique alphanumeric string.
    """
    request = context.get("request")
    if request:
        attribute_name = "__last_unique_id"
        if not hasattr(request, attribute_name):
            setattr(request, attribute_name, 0)
        id = getattr(request, attribute_name) + 1
        setattr(request, attribute_name, id)
        return id

    else:
        return get_unique_id()


def search_gov_affiliate(context):
    """Given a request, return the appropriate affiliate for Search.gov.

    Our default affiliate code is "cfpb". We have a separate Spanish-language
    index named "cfpb_es". We then have two additional indexes, "cfpb_beta"
    and "cfpb_beta_es", for use on beta.consumerfinance.gov.
    """
    affiliate = "cfpb"

    if environment_is("beta"):
        affiliate += "_beta"

    language = context.get("language")
    if language == "es":
        affiliate += "_es"

    return affiliate


class V1Extension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update(
            {
                "category_label": ref.category_label,
                "choices_for_page_type": ref.choices_for_page_type,
                "get_category_icon": ref.get_category_icon,
                "get_unique_id": get_unique_id,
                "is_filter_selected": pass_context(is_filter_selected),
                "unique_id_in_context": pass_context(unique_id_in_context),
                "app_url": app_url,
                "app_page_url": app_page_url,
                "search_gov_affiliate": pass_context(search_gov_affiliate),
            }
        )


# Nicer import names
datetimes_extension = DatetimesExtension
images_extension = ImagesExtension
v1_extension = V1Extension
