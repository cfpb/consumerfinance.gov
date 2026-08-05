from django import template
from django.utils.safestring import SafeString, mark_safe


register = template.Library()


@register.simple_tag()
def svg_icon(name: str, spin: bool = False) -> SafeString:
    """Return cfpb-icon web component."""
    spin_attr = " spin" if spin else ""
    return mark_safe(f'<cfpb-icon name="{name}"{spin_attr}></cfpb-icon>')
