from django import template
from django.conf import settings
import HTMLParser
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter()
def unescape(value):
    return mark_safe(HTMLParser.HTMLParser().unescape(value))
