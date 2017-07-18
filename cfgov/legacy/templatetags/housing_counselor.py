from __future__ import unicode_literals

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def split_string_list(s):
    """Split a comma-separated string as returned by the django-hud API.

    See how services and languages are returned by the Command class in
    hud_api_replace.management.commands.load_hud_data.
    """
    return [x.strip().replace('&#44;', ',') for x in s.split(',')]
