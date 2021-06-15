from django.urls import path, re_path
from django.urls.conf import include
from django.views.generic import TemplateView

from wagtailsharing.views import ServeView

from . import views

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
    ),

    # Handle results (assumes you have signed cookie "resultsUrl")
    re_path(
        r'^assess/results/$',
        views.assessment_results,
        name='assessment_results'
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
            # Handle redirect to step1
            path('', assessment_view, name=f'assessment_{key}'),
            # URLs for particular steps
            re_path(
                r'^(?P<step>.+)/$',
                assessment_view,
                name=f'assessment_{key}_step'
            ),
        ]))
    )
