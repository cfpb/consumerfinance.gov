from django.conf.urls import url
from django.views.generic import TemplateView

from diversity_inclusion.views import GetAssessmentForm


urlpatterns = [
    url(
        r'^voluntary-assessment-onboarding-form/$',
        GetAssessmentForm.as_view(),
        name='voluntary_assessment_form'
    ),
    url(
        r'^voluntary-assessment-onboarding-form/privacy-act-statement/$',
        TemplateView.as_view(
            template_name='diversity_inclusion/privacy.html'
        ),
        name='privacy'
    ),
]
