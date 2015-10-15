from django.shortcuts import render

# Create your views here.

def server_error(request, template_name='404.html'):
    from django.template import RequestContext
    from django.http import HttpResponseServerError
    t = get_template(template_name)
    return HttpResponseServerError(t.render(RequestContext(request)))
