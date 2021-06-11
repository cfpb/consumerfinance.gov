from django.urls import path, re_path
from django.views.generic import TemplateView

from .forms import form_lists
from .views import AssessmentWizard

from wagtailsharing.views import ServeView


# Create view wrappers for our assessments. Note the AssessmentWizard
# won't be instantiated until the view needs it.
wizards = {}
for k, form_list in form_lists.items():
    wizards[k] = AssessmentWizard.as_view(
        form_list=form_list,
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

    # TODO figure out how to parse out the <elem>
    path(
        'assess/elem/results/',
        TemplateView.as_view(
            template_name='teachers_digital_platform/survey-results.html',
        )
    ),
    re_path(
        r'^assess/elem/(?P<step>.+)/$',
        wizards['elem'],
        name='survey_step'
    ),
    path('assess/elem/', wizards['elem'], name='survey'),

    re_path(
        r'^$',
        lambda request: ServeView.as_view()(request, request.path)
    )
]
