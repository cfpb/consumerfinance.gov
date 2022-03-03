import json

from django import template

register = template.Library()


@register.filter
def jsonify(obj):
    return json.dumps(obj)
