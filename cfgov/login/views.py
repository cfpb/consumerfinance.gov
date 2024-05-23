from django.conf import settings

from wagtail.admin.views.account import LoginView as WagtailLoginView


class LoginView(WagtailLoginView):
    template_name = "login/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sso_enabled"] = settings.ENABLE_SSO
        return context
