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

    re_path(
        r'^$',
        lambda request: ServeView.as_view()(request, request.path)
    ),

    # Handle all results (expects signed cookie "resultsUrl")
    re_path(
        r'^assess/results/$',
        views.student_results,
        name='tdp_assess_student_results',
    ),

    # View a shared results page (expects ?r=...signed value)
    re_path(
        r'^assess/view/$',
        views.view_results,
        name='tdp_assess_view_results',
    ),
]

# Our wizards are set up here. For each assessment, it's created from
# loading JSON, its questions are burned into attributes on new form
# classes for each page, and a view is created from those form classes.
# Below we set up paths for each assessment view
for key, assessment_view in views.AssessmentWizard.build_views().items():
    urlpatterns.append(
        # Base URL for this assessment
        path(f'assess/{key}/', include([
            # Handle redirect to assessment intro
            path(
                '',
                TemplateView.as_view(
                    template_name=f'{tdp}/assess/intro-{key}.html'
                ),
                name=f'assessment_{key}_intro',
            ),
            # URLs for particular steps
            re_path(
                r'^(?P<step>.+)/$',
                assessment_view,
                name=f'assessment_{key}_step'
            ),
        ]))
    )
