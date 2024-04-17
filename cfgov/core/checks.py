from django.core.checks import Error, Tags, register
from django.core.checks.security.base import check_secret_key


# This converts Django's built-in security.W009 warning to an error to comply
# with our baseline requirements.
@register(Tags.security, deploy=True)
def check_secret_key_and_error(app_configs, **kwargs):
    warnings = check_secret_key(app_configs, **kwargs)
    return [
        Error(warning.msg, hint=warning.hint, id=warning.id)
        for warning in warnings
    ]
