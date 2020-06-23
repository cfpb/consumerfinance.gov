from django.urls import re_path
from django.views.generic import TemplateView

from wagtailsharing.views import ServeView


urlpatterns = [
    re_path(
        r'^curriculum-review/tool/$',
        TemplateView.as_view(template_name='crtool/crt-survey.html')
    ),

    re_path(
        r'^curriculum-review/before-you-begin/$',
        TemplateView.as_view(template_name='crtool/crt-start.html')
    ),

    re_path(
        r'^journey',
        TemplateView.as_view(template_name='crtool/bb-tool.html')
    ),

    re_path(
        r'^$',
        lambda request: ServeView.as_view()(request, request.path)
    )
]
