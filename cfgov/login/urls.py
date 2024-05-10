from django.conf import settings
from django.urls import include, re_path, reverse_lazy
from django.views.generic.base import RedirectView


if settings.ENABLE_SSO:  # pragma: no cover
    urlpatterns = [
        # If SSO auth is enabled, /login will redirect to /oidc/login,
        # which in turn will redirect to the configured identity provider.
        re_path(r"^oidc/", include("mozilla_django_oidc.urls")),
        re_path(
            r"^admin/login/$",
            RedirectView.as_view(
                url=reverse_lazy("oidc_authentication_init"), query_string=True
            ),
        ),
        re_path(
            r"^admin/logout/$",
            RedirectView.as_view(
                url=reverse_lazy("oidc_logout"),
                query_string=True,
            ),
        ),
    ]
else:
    urlpatterns = [
        # When SSO is not enabled, the Django login should redirect to Wagtail
        re_path(
            r"^django-admin/login/$",
            RedirectView.as_view(
                url=reverse_lazy("wagtailadmin_login"), query_string=True
            ),
        ),
    ]

urlpatterns = urlpatterns + [
    # Redirect root-level /login and /logout to Wagtail's URLs
    re_path(
        r"^login/$",
        RedirectView.as_view(
            url=reverse_lazy("wagtailadmin_login"), query_string=True
        ),
    ),
    re_path(
        r"^logout/$",
        RedirectView.as_view(
            url=reverse_lazy("wagtailadmin_logout"), query_string=True
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
