from django.views.generic import TemplateView

from diversity_inclusion.views import GetAssessmentForm


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


urlpatterns = [
    re_path(
        r"^voluntary-assessment-onboarding-form/$",
        GetAssessmentForm.as_view(),
        name="voluntary_assessment_form",
    ),
    re_path(
        r"^voluntary-assessment-onboarding-form/form-submitted/$",
        TemplateView.as_view(
            template_name="diversity_inclusion/form-submitted.html"
        ),
        name="form_submitted",
    ),
    re_path(
        r"^voluntary-assessment-onboarding-form/privacy-act-statement/$",
        TemplateView.as_view(
            template_name="diversity_inclusion/privacy.html"
        ),
        name="privacy",
    ),
]
