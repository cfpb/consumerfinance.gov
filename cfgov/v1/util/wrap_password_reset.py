from functools import wraps

from django.http import Http404

from wagtail.admin.views import account


# This wrapper is used to check our custom password-reset routine, in urls.py:
# https://github.com/cfpb/consumerfinance.gov/blob/6360823ec447cba6527d128edcd55ecae5186c59/cfgov/cfgov/urls.py#L554-L557  # noqa
# In Wagtail 2, it was converted to a mixin (PasswordResetEnabledViewMixin)
# and used to build reset views, as opposed to wrapping them.
# We may want to follow that pattern in our password routine, or review
# our entire custom setup, but this PR is too big already.
# So for now, we resurrect the wrapper to serve our custom routine.
def _wrap_password_reset_view(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not account.password_reset_enabled():
            raise Http404
        return view_func(*args, **kwargs)

    return wrapper
