from django.conf import settings
from django.contrib.auth import views as django_auth_views
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView

from login.forms import CFGOVPasswordChangeForm
from login.views import CFGOVPasswordResetConfirmView, change_password


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
    # Override Wagtail and Django password views to enforce our password policy
    re_path(
        r"^django-admin/password_change",
        change_password,
        name="django_admin_account_change_password",
    ),
    path(
        "admin/password_reset/confirm/<uidb64>/<token>/",
        CFGOVPasswordResetConfirmView.as_view(),
        name="wagtailadmin_password_reset_confirm",
    ),
    re_path(
        r"^django-admin/password_change",
        django_auth_views.PasswordChangeView.as_view(),
        {"password_change_form": CFGOVPasswordChangeForm},
    ),
    re_path(
        r"^password/change/done/$",
        django_auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    re_path(
        r"^admin/account/change_password/$",
        change_password,
        name="wagtailadmin_account_change_password",
    ),
]
