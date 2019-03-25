from six.moves import html_parser as HTMLParser

from django.utils.module_loading import import_string

from jinja2 import Markup, contextfunction
from jinja2.ext import Extension

from hmda.templatetags.hmda_banners import hmda_outage_banner
from v1.jinja2tags.datetimes import DatetimesExtension
from v1.jinja2tags.fragment_cache import FragmentCacheExtension
from v1.models import CFGOVRendition
from v1.templatetags.complaint_banners import (
    complaint_issue_banner, complaint_maintenance_banner
)
from v1.templatetags.email_popup import email_popup
from v1.templatetags.mega_menu import get_menu_items
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
    if image:
        block_alt = image.get('alt')
        upload = image.get('upload')

        if block_alt:
            return block_alt
        elif upload and upload.alt:
            return upload.alt

    return ''


def is_filter_selected(context, fieldname, value):
    request_get = context['request'].GET

    query_string_values = [
        k for k in
        request_get.getlist(fieldname) +
        request_get.getlist('filter_' + fieldname)
        if k
    ]

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
    html = template.render(new_context)
    unescaped = HTMLParser.HTMLParser().unescape(html)
    # Return the rendered template as safe html
    return Markup(unescaped)


class V1Extension(Extension):
    def __init__(self, environment):
        super(V1Extension, self).__init__(environment)

        self.environment.globals.update({
            'category_label': ref.category_label,
            'choices_for_page_type': ref.choices_for_page_type,
            'email_popup': email_popup,
            'complaint_issue_banner': complaint_issue_banner,
            'complaint_maintenance_banner': complaint_maintenance_banner,
            'fcm_label': ref.fcm_label,
            'get_menu_items': get_menu_items,
            'get_model': get_model,
            'get_unique_id': get_unique_id,
            'hmda_outage_banner': hmda_outage_banner,
            'image_alt_value': image_alt_value,
            'is_blog': ref.is_blog,
            'is_report': ref.is_report,
            'is_filter_selected': contextfunction(is_filter_selected),
            'render_stream_child': contextfunction(render_stream_child),
        })


# Nicer import names
datetimes_extension = DatetimesExtension
fragment_cache_extension = FragmentCacheExtension
v1_extension = V1Extension
