from django.urls import re_path
from django.views.generic import TemplateView

from wagtailsharing.views import ServeView


urlpatterns = [
    re_path(
        r'^journey',
        TemplateView.as_view(
            template_name='teachers_digital_platform/bb-tool.html'
        )
    ),

    re_path(
        r'^$',
        lambda request: ServeView.as_view()(request, request.path)
    )
]
