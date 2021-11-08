from django.views.generic import TemplateView

from flags.urls import flagged_re_path
from privacy.views import GetRecordsAccessForm, GetDisclosureConsentForm


urlpatterns = [
    flagged_re_path(
        "PRIVACY_FORMS",
        r"^disclosure-consent/$",
        GetDisclosureConsentForm.as_view(),
        name="disclosure_consent",
    ),
    flagged_re_path(
        "PRIVACY_FORMS",
        r"^records-access/$",
        GetRecordsAccessForm.as_view(),
        name="records_access",
    ),
    flagged_re_path(
        "PRIVACY_FORMS",
        r"^test-form/form-submitted/$",
        TemplateView.as_view(
            template_name="privacy/form-submitted.html"
        ),
        name="form_submitted",
    ),
    flagged_re_path(
        "PRIVACY_FORMS",
        r"^privacy-act-statement/$",
        TemplateView.as_view(
            template_name="privacy/privacy.html"
        ),
        name="privacy_statement",
    ),
]
