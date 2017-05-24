from __future__ import unicode_literals

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def split_services(s):
    """Prepares the list of services returned by the django-hud API.

    See hud_api_replace.management.commands.Command.translate_services.
    """
    return [service.strip().replace('&#44;', ',') for service in s.split(',')]
