from django.urls import path, re_path
from django.urls.conf import include
from django.views.generic import TemplateView

from wagtailsharing.views import ServeView

from . import views


tdp = 'teachers_digital_platform'

urlpatterns = [
    re_path(
        r'^journey',
        TemplateView.as_view(
            template_name=f'{tdp}/bb-tool.html'
        )
    ),

    path(
        r'',
        lambda request: ServeView.as_view()(request, request.path)
    ),

    # Temporary, remove after wagtail page added
    path(
        r'surveys/',
        TemplateView.as_view(
            template_name=f'{tdp}/survey/intro.html'
        ),
        name='tdp_survey_intro',
    ),

    # Handle all results (expects signed cookie "resultsUrl")
    path(
        r'surveys/results/',
        views.student_results,
        name='tdp_survey_student_results',
    ),

    # View a shared results page (expects ?r=...signed value)
    path(
        r'surveys/view/',
        views.view_results,
        name='tdp_survey_view_results',
    ),
]

# Our wizards are set up here. For each survey, it's created from
# loading JSON, its questions are burned into attributes on new form
# classes for each page, and a view is created from those form classes.
# Below we set up paths for each survey view
for key, survey_view in views.SurveyWizard.build_views().items():
    urlpatterns.append(
        # Base URL for this survey
        path(f'surveys/{key}/', include([
            # Handle redirect to grade-level intro page
            path(
                '',
                views.create_grade_level_page_handler(key),
                name=f'survey_{key}_grade_level',
            ),
            # URLs for particular steps
            re_path(
                r'^(?P<step>.+)/$',
                survey_view,
                name=f'survey_{key}_step'
            ),
        ]))
    )
