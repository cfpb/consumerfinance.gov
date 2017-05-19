from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import urlize

from core.utils import signed_redirect as signed_redirect_fn


register = template.Library()


@register.filter
@stringfilter
def signed_redirect(url):
    return signed_redirect_fn(url)


@register.filter
@stringfilter
def is_url(url):
    return urlize(url) != url
