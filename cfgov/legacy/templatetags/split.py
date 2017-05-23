from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split(s, delimiter):
    """
        Returns the string turned into a list.
    """
    return s.split(delimiter)
