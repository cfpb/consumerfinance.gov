from django.conf import settings
from django.conf.urls import include
from wagtail.wagtailcore.views import serve as wagtail_serve


def wagtail_fail_through(request):
    return wagtail_serve(request, request.path)


def include_if_app_enabled(app_name, module_or_name, namespace=None):
    if app_name in settings.INSTALLED_APPS:
        return include(module_or_name, namespace=namespace)
    return wagtail_fail_through
