import six

from django import template


register = template.Library()


@register.simple_tag
def app_url(request):
    if six.PY2:  # pragma: no cover
        return request.path.split('/')[1].encode('ascii', 'ignore')

    return request.path.split('/')[1]


@register.simple_tag
def app_page_url(request):
    if six.PY2:  # pragma: no cover
        return request.path[1:].encode('ascii', 'ignore')

    return request.path[1:]
