from django.conf import settings
from django.core.checks import Info, Tags, register


@register(Tags.security)
def check_oidc_admin_role_setting(app_configs, **kwargs):
    errors = []

    if settings.ENABLE_SSO and settings.OIDC_OP_ADMIN_ROLE is None:
        errors.append(
            Info(
                (
                    "SSO is enabled, but OIDC_OP_ADMIN_ROLE not set, "
                    "is_superuser will not be modified for any users."
                ),
                hint=(
                    "If the SSO provider supports user role claims, "
                    "set OIDC_OP_ADMIN_ROLE to the role identifier used for "
                    "admin users."
                ),
                id="login.I001",
            )
        )

    return errors
