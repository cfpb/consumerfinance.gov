from django.conf import settings
from django.urls import re_path
from django.views.generic import RedirectView


urlpatterns = [
    # Redirect all requests under /f/ to the public-facing S3 domain,
    # usually files.consumerfinance.gov.
    re_path(
        r"^f/(?P<path>.*)$",
        RedirectView.as_view(
            url=f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/f/%(path)s",
            permanent=False,
        ),
    ),
]
