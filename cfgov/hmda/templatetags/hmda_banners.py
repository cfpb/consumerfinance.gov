from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def hmda_outage_banner(request):
    template = 'hmda-outage-banner.html'
    return mark_safe(render_to_string(template))
