from django.views.generic.base import TemplateView
from django.http import HttpResponse

class ServiceWorkerView(TemplateView):
    template_name = 'mmt-my-money-calendar/service-worker.js'
    content_type = 'application/javascript'
    scope = '/'

    def dispatch(self, request, *args, **kwargs):
        response = super(ServiceWorkerView).dispatch(self, request, *args, **kwargs)
        response['Service-Worker-Allowed'] = self.scope
        return response
