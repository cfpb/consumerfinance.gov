import logging

from django import template
from django.utils.safestring import SafeString, mark_safe


logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag()
def svg_icon(name: str, spin: bool = False) -> SafeString:
    spin_attr = " spin" if spin else ""
    """Return cfpb-icon web component."""
    return mark_safe(f'<cfpb-icon name="{name}"{spin_attr}></cfpb-icon>')
