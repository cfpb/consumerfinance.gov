from django.views.generic import TemplateView

from foia.views import GetRequestForm

from flags.urls import flagged_re_path


urlpatterns = [
    flagged_re_path(
        "TEST_FOIA_FORM",
        r"^foia-request-form/$",
        GetRequestForm.as_view(),
        name="foia_form",
    ),
    flagged_re_path(
        "TEST_FOIA_FORM",
        r"^foia-request-form/form-submitted/$",
        TemplateView.as_view(
            template_name="foia/form-submitted.html"
        ),
        name="foia_form_submitted",
    ),
]
