from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from django.views.generic import TemplateView


class TemplateDebugView(TemplateView):
    template_name = 'v1/template_debug.html'
    debug_template_name = None
    debug_test_cases = None
    extra_js = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.debug_template_name is None or self.debug_test_cases is None:
            raise ImproperlyConfigured(
                "TemplateDebugView requires definition of "
                "debug_template_name and debug_test_cases"
            )

        template = loader.get_template(self.debug_template_name)

        context.update({
            'debug_template_name': self.debug_template_name,
            'debug_test_cases': {
                name: template.render({
                    'request': self.request,
                    'value': data,
                }) for name, data in self.debug_test_cases.items()
            },
        })

        if self.extra_js:
            context['page'] = {
                'media': self.extra_js,
            }

        return context
