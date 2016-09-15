from django.http import Http404
from django.utils.functional import wraps

from flags.template_functions import flag_enabled


def flag_required(name, fallback_view=None):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if flag_enabled(request, name):
                return func(request, *args, **kwargs)
            elif fallback_view is not None:
                return fallback_view(request, *args, **kwargs)
            else:
                raise Http404

        return wraps(func)(inner)

    return decorator
