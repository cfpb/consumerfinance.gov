from django import template
from django.template.defaultfilters import stringfilter

from core.utils import signed_redirect as signed_redirect_fn


register = template.Library()


@register.filter
@stringfilter
def signed_redirect(url):
    return signed_redirect_fn(url)
