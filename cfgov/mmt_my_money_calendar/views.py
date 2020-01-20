from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.http import HttpResponse

class ServiceWorkerView(TemplateView):
    template_name = 'mmt-my-money-calendar/service-worker.js'
    content_type = 'application/javascript'
    scope = '/'

    """
    Adds a Service-Worker-Allowed HTTP response header when clients request a service worker script.
    Can be used to properly set the service worker's allowed path scope since it comes from a different
    location (/static) than whichever app it's meant to operate on.

    See: https://www.w3.org/TR/service-workers/#service-worker-allowed
    """
    def dispatch(self, request, *args, **kwargs):
        response = super(ServiceWorkerView, self).dispatch(request, *args, **kwargs)
        response['Service-Worker-Allowed'] = self.scope
        return response
