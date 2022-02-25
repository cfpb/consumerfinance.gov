import html

from django.utils.module_loading import import_string

from jinja2 import Markup, contextfunction
from jinja2.ext import Extension

from core.feature_flags import environment_is
from v1.jinja2tags.datetimes import DatetimesExtension
from v1.jinja2tags.fragment_cache import FragmentCacheExtension
from v1.models.images import CFGOVRendition
from v1.templatetags.app_urls import app_page_url, app_url
from v1.templatetags.email_popup import email_popup
from v1.util import ref
from v1.util.util import get_unique_id


def get_model(model_name):
    model_class = import_string(model_name)
    return model_class


def image_alt_value(image):
    """Given an ImageBasic block or a CFGOVImage rendition as `image`,
    return the appropriate alt text.

    Return the CFGOVImage rendition's alt field, if present.
    Returns the alt field from the block, if it is set.
    Otherwise, returns the alt field from the CFGOVImage object, if it is set.
    Otherwise, returns an empty string.
    """

    # Check to see if the passed value is a CFGOVRendition
    if isinstance(image, CFGOVRendition):
        return image.alt

    # Otherwise, if it is a block
    if image and hasattr(image, 'get'):
        block_alt = image.get('alt')
        upload = image.get('upload')

        if block_alt:
            return block_alt
        elif upload and upload.alt:
            return upload.alt

    return ''


def is_filter_selected(context, fieldname, value):
    """Check URL query parameters to see if a filter option should be selected

    Returns True if fieldname=value is found in the GET data in order to output
    the `checked` attribute on a checkbox or radio button in the
    _filter_selectable macro (see: filterable-list-controls.html).
    """
    request_get = context['request'].GET

    query_string_values = [
        k for k in
        request_get.getlist(fieldname) +
        request_get.getlist('filter_' + fieldname)
        if k
    ]

    # Dirty hack to check the default option for the `archived` filter
    if fieldname == 'archived' and value == 'include':
        return True

    return value in query_string_values


def render_stream_child(context, stream_child):
    # Use the django_jinja to get the template content based on its name
    try:
        template = context.environment.get_template(
            stream_child.block.meta.template)
    except Exception:
        return stream_child

    # Create a new context based on the current one as we can't edit it
    # directly
    new_context = context.get_all()
    # Add the value on the context (value is the keyword chosen by
    # wagtail for the blocks context)
    try:
        new_context['value'] = stream_child.value
    except AttributeError:
        new_context['value'] = stream_child

    # Render the template with the context
    html_result = template.render(new_context)
    unescaped = html.unescape(html_result)
    # Return the rendered template as safe html
    return Markup(unescaped)


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
    request = context.get('request')
    if request:
        attribute_name = '__last_unique_id'
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
    affiliate = 'cfpb'

    if environment_is('beta'):
        affiliate += '_beta'

    language = context.get('language')
    if language == 'es':
        affiliate += '_es'

    return affiliate


class V1Extension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update({
            'category_label': ref.category_label,
            'choices_for_page_type': ref.choices_for_page_type,
            'email_popup': email_popup,
            'get_model': get_model,
            'get_unique_id': get_unique_id,
            'image_alt_value': image_alt_value,
            'is_blog': ref.is_blog,
            'is_event': ref.is_event,
            'is_report': ref.is_report,
            'is_filter_selected': contextfunction(is_filter_selected),
            'render_stream_child': contextfunction(render_stream_child),
            'unique_id_in_context': contextfunction(unique_id_in_context),
            'app_url': app_url,
            'app_page_url': app_page_url,
            'search_gov_affiliate': contextfunction(search_gov_affiliate),
        })


# Nicer import names
datetimes_extension = DatetimesExtension
fragment_cache_extension = FragmentCacheExtension
v1_extension = V1Extension
