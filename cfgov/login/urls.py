from django.conf import settings
from django.urls import include, re_path, reverse_lazy
from django.views.generic.base import RedirectView

from login.views import LoginView


urlpatterns = [
    # Include OIDC URLs
    re_path(r"^oidc/", include("mozilla_django_oidc.urls")),
    # Override Wagtail's login URL with our subclass
    re_path(r"^admin/login/", LoginView.as_view(), name="cfgov_login"),
    # Redirect root-level /login and /logout
    re_path(
        r"^login/$",
        RedirectView.as_view(
            url=reverse_lazy("cfgov_login"), query_string=True
        ),
    ),
    re_path(
        r"^logout/$",
        RedirectView.as_view(
            url=reverse_lazy("cfgov_login"), query_string=True
        ),
    ),
    # Redirect the Django admin login to Wagtail
    re_path(
        r"^django-admin/login/$",
        RedirectView.as_view(
            url=reverse_lazy("cfgov_login"), query_string=True
        ),
    ),
    # Redirect Django's password change view to Wagtail's
    re_path(
        r"^django-admin/password_change",
        RedirectView.as_view(
            url=reverse_lazy("wagtailadmin_password_reset"), query_string=True
        ),
    ),
]

if settings.ENABLE_SSO:  # pragma: no cover
    urlpatterns = urlpatterns + [
        # Redirect logout to the OIDC logout to make sure we clear our OIDC
        # session information
        re_path(
            r"^admin/logout/$",
            RedirectView.as_view(
                url=reverse_lazy("oidc_logout"),
                query_string=True,
            ),
        ),
    ]
