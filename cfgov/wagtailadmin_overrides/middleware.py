from django.conf import settings
from django.urls.utils import get_callable

from wagtail.admin.auth import require_admin_access


# Override certain Wagtail admin views. Intercepts the processing of the
# default view and replaces it with a replacement if one has been defined.
#
# Inspired by https://github.com/wagtail/wagtail/issues/6166.
class WagtailAdminViewOverrideMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        replacement_views = getattr(
            settings, "WAGTAILADMIN_OVERRIDDEN_VIEWS", {}
        )

        view = replacement_views.get(request.resolver_match.view_name)

        # If we're not overriding this view, return None so that the default
        # view will be invoked instead.
        if not view:
            return None

        view = get_callable(view)

        return require_admin_access(view)(request, *view_args, **view_kwargs)
