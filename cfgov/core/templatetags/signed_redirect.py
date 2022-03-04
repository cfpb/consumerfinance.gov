from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import urlize


register = template.Library()


@register.filter
@stringfilter
def is_url(url):
    return urlize(url) != url
