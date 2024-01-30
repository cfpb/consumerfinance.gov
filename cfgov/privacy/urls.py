from django.urls import re_path
from django.views.generic import TemplateView

from privacy.views import GetDisclosureConsentForm, GetRecordsAccessForm


urlpatterns = [
    re_path(
        r"^disclosure-consent/$",
        GetDisclosureConsentForm.as_view(),
        name="disclosure_consent",
    ),
    re_path(
        r"^records-access/$",
        GetRecordsAccessForm.as_view(),
        name="records_access",
    ),
    re_path(
        r"^form-submitted/$",
        TemplateView.as_view(template_name="privacy/form-submitted.html"),
        name="form_submitted",
    ),
]
