from django.conf import settings
from django.contrib.auth import views as django_auth_views
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

from login.forms import CFGOVPasswordChangeForm
from login.views import (
    CFGOVPasswordResetConfirmView,
    change_password,
    check_permissions,
    login_with_lockout,
)


if settings.SAML_AUTH:  # pragma: no cover
    urlpatterns = [
        # If SAML2 auth is enabled, /login will redirect to /saml2/login,
        # which in turn will redirect to the configured identity provider.
        re_path(r"saml2/", include("djangosaml2.urls")),
        # For backup/admin/emergency auth in the event that SSO is down,
        # the Django login is available at /django-admin/login. Wagtail's
        # /admin/login is redirected to /login for both SSO and non-SSO auth.
        re_path(
            r"^login/$",
            RedirectView.as_view(url="/saml2/login/", query_string=True),
        ),
        re_path(
            r"^logout/$",
            RedirectView.as_view(
                url="/saml2/logout/",
                query_string=True,
            ),
            name="logout",
        ),
    ]
else:
    urlpatterns = [
        re_path(r"^login/$", login_with_lockout, name="cfpb_login"),
        # When SSO is not enabled, the Django login should redirect to our
        # /login URL, added above.
        re_path(
            r"^django-admin/login/$",
            RedirectView.as_view(url="/login/", query_string=True),
        ),
        re_path(
            r"^logout/$", django_auth_views.LogoutView.as_view(), name="logout"
        ),
    ]

urlpatterns = urlpatterns + [
    # Wagtail will always redirect to /admin/login when login is required in
    # the admin. This will redirect /admin/login to /login, which is handled
    # by the SSO and non-SSO patterns above.
    re_path(
        r"^admin/login/$",
        RedirectView.as_view(url="/login/", permanent=True, query_string=True),
    ),
    re_path(
        r"^login/check_permissions/$",
        check_permissions,
        name="check_permissions",
    ),
    re_path(
        r"^django-admin/password_change",
        change_password,
        name="django_admin_account_change_password",
    ),
    # Override Wagtail password views with our password policy
    path(
        "admin/password_reset/confirm/<uidb64>/<token>/",
        CFGOVPasswordResetConfirmView.as_view(),
        name="wagtailadmin_password_reset_confirm",
    ),
    # Override Django password change views
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
