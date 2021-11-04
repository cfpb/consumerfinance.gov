from django.views.generic import TemplateView

from flags.urls import flagged_re_path
from foia.views import GetRequestForm


urlpatterns = [
    flagged_re_path(
        "TEST_UPLOAD_FORM",
        r"^test-form/$",
        GetRequestForm.as_view(),
        name="foia_form",
    ),
    flagged_re_path(
        "TEST_UPLOAD_FORM",
        r"^test-form/form-submitted/$",
        TemplateView.as_view(
            template_name="foia/form-submitted.html"
        ),
        name="foia_form_submitted",
    ),
]
