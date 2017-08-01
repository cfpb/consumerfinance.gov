
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import View, TemplateView, RedirectView
from flags.state import flag_state
from sheerlike.views.generic import SheerTemplateView
from wagtailsharing.views import ServeView


class OahServeView(View):

    def get(self, request, path):
        return self.getResponse(path)

    def is_resource_request(self, path):
        return 'resources/' in path

    def get_resource_response(self, resource_url):
        return RedirectView.as_view(url=resource_url,
                                    permanent=True)(self.request)

    def get_template_response(self, as_view, template_name):
        try:
            get_template(template_name)
        except TemplateDoesNotExist:
            return ServeView.as_view()(self.request, self.request.path)
        else:
            return as_view(template_name=template_name)(self.request)

    def getResponse(self, path):
        template_name = path + ( '' if 'index.html' in path else '/index.html' )
        print template_name
        resource_url = '/static/owning-a-home/' + path
        as_view = SheerTemplateView.as_view

        if flag_state('OAH_DESHEERING', request=self.request):
            template_name = 'owning-a-home/' + template_name
            as_view = TemplateView.as_view

        if self.is_resource_request(path):
            return self.get_resource_response(resource_url)

        return self.get_template_response(as_view, template_name)
