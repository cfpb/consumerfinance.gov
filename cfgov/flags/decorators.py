from django.http import Http404
from django.utils.functional import wraps

from flags.template_functions import flag_enabled


def flag_required(flag_name, fallback_view=None, pass_if_set=True):
    def decorator(func):
        def inner(request, *args, **kwargs):
            enabled = flag_enabled(request, flag_name)

            if (enabled and pass_if_set) or (not enabled and not pass_if_set):
                return func(request, *args, **kwargs)
            elif fallback_view is not None:
                return fallback_view(request)
            else:
                raise Http404

        return wraps(func)(inner)

    return decorator
