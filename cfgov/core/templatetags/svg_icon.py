import logging

from django import template
from django.utils.safestring import SafeString, mark_safe


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag()
def svg_icon(name: str) -> SafeString:
    """Return cfpb-icon web component."""
    return mark_safe(f'<cfpb-icon name="{name}"></cfpb-icon>')
