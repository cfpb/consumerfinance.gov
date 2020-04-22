from django.urls import re_path

from wagtail.core import hooks

from v1.views.template_debug import TemplateDebugView

from .notification import notification_test_cases  # noqa 401


def register_template_debug(app_name, url_path, template_name, test_cases):
    @hooks.register("register_admin_urls")
    def register_template_debug_url():
        return [
            re_path(
                rf"^template_debug/{app_name}/{url_path}/",
                TemplateDebugView.as_view(
                    debug_template_name=template_name,
                    debug_test_cases=test_cases,
                ),
                name=f"template_debug_{app_name}_{url_path}",
            ),
        ]
