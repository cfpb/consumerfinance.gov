from threading import local
from django.http import HttpResponse
from django.core.urlresolvers import resolve

_active = local()

def get_request():
    return _active.request

class FlaskyHeaderGetter(object):
    def __init__(self, request):
        self.request= request

    def __getitem__(self, key):
        django_key = 'HTTP_' + key.upper().replace('-','_')
        return self.request.META.get(django_key)

    def get(self, key):
        return self.__getitem__(key)



class GlobalRequestMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        _active.request = request
        request.headers = FlaskyHeaderGetter(request)
        request.url = "%s://%s%s" % (request.scheme, request.get_host(),
                request.get_full_path())
        request.url_rule = request.resolver_match
        request.url_rule.endpoint = request.resolver_match.url_name
        return None
