from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponseServerError


def server_error(request, template_name='404.html'):
    t = get_template(template_name)
    return HttpResponseServerError(t.render(RequestContext(request)))
