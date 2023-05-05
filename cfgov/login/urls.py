from django.conf import settings
from django.urls import include, re_path, reverse_lazy
from django.views.generic.base import RedirectView


if settings.SAML_AUTH:  # pragma: no cover
    urlpatterns = [
        # If SAML2 auth is enabled, /login will redirect to /saml2/login,
        # which in turn will redirect to the configured identity provider.
        re_path(r"saml2/", include("djangosaml2.urls")),
        # Redirect the Wagtail login/logout views to djangosaml2.
        # For admin authentication, /django-admin/login is preserved when SSO
        # is enabled.
        re_path(
            r"^/admin/login/$",
            RedirectView.as_view(
                url=reverse_lazy("saml2_login"), query_string=True
            ),
        ),
        re_path(
            r"^/admin/logout/$",
            RedirectView.as_view(
                url=reverse_lazy("saml2_logout"),
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
    # Redirect root-level /login and /logout to Wagtail.
    # If SSO is enabled, these will redirect from there to djangosaml2.
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
