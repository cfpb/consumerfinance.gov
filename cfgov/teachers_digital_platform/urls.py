from django.urls import path, re_path
from django.views.generic import TemplateView

from teachers_digital_platform.forms import get_pages
from teachers_digital_platform.views import SurveyWizard

from wagtailsharing.views import ServeView


pages = get_pages('gr3')

contact_wizard = SurveyWizard.as_view(
    form_list=pages['form_list'],
    url_name='survey_step',
    template_name='teachers_digital_platform/survey-page.html',
)

urlpatterns = [
    re_path(
        r'^journey',
        TemplateView.as_view(
            template_name='teachers_digital_platform/bb-tool.html'
        )
    ),

    path(
        'survey/results/',
        TemplateView.as_view(
            template_name='teachers_digital_platform/survey-results.html'
        )
    ),

    re_path(
        r'^survey/(?P<step>.+)/$',
        contact_wizard,
        name='survey_step'
    ),

    path('survey/', contact_wizard, name='survey'),

    re_path(
        r'^$',
        lambda request: ServeView.as_view()(request, request.path)
    )
]
