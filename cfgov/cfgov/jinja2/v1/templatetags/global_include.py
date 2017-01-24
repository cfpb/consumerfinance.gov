from django import template

import sheerlike

register = template.Library()


@register.simple_tag
def global_include(name):
    return sheerlike.global_render_template(name)
