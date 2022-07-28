from wagtail.core import hooks

from v1.views.template_debug import TemplateDebugView

from .call_to_action import call_to_action_test_cases  # noqa 401
from .featured_content import featured_content_test_cases  # noqa 401
from .heading import heading_test_cases  # noqa 401
from .notification import notification_test_cases  # noqa 401
from .video_player import video_player_test_cases  # noqa 401


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


def register_template_debug(
    app_name, url_path, template_name, test_cases, extra_js=None
):
    @hooks.register("register_admin_urls")
    def register_template_debug_url():
        return [
            re_path(
                rf"^template_debug/{app_name}/{url_path}/",
                TemplateDebugView.as_view(
                    debug_template_name=template_name,
                    debug_test_cases=test_cases,
                    extra_js=extra_js,
                ),
                name=f"template_debug_{app_name}_{url_path}",
            ),
        ]
