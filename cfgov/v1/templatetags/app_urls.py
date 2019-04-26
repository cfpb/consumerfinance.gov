from django import template


register = template.Library()


@register.simple_tag
def app_url(request):
    return request.path.split('/')[1].encode('ascii', 'ignore')


@register.simple_tag
def app_page_url(request):
    return request.path[1:].encode('ascii', 'ignore')
