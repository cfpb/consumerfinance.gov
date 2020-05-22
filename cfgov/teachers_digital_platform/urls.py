from django.urls import re_path
from django.views.generic import TemplateView

from wagtailsharing.views import ServeView


urlpatterns = [
    re_path(
        r'^curriculum-review/tool/$',
        TemplateView.as_view(template_name='teachers_digital_platform/crt-survey.html')  # noqa: E501
    ),

    re_path(
        r'^curriculum-review/before-you-begin/$',
        TemplateView.as_view(template_name='teachers_digital_platform/crt-start.html')  # noqa: E501
    ),

    re_path(
        r'^journey',
        TemplateView.as_view(template_name='teachers_digital_platform/bb-tool.html')  # noqa: E501
    ),

    re_path(
        r'^$',
        lambda request: ServeView.as_view()(request, request.path)  # noqa: E501
    )
]
