from django import template
from django.template import loader


register = template.Library()


@register.simple_tag()
def svg_icon(string):
    return loader.get_template('icons/' + string + '.svg').render()
