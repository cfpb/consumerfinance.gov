import re
from functools import partial

from django.urls import re_path
from django.views.generic import RedirectView


urlpatterns = []


def make_redirect(pattern, target, permanent=True, append_to=None):
    """Create Django redirect from source pattern and target URL.

    pattern: URL regex pattern to match (without leading / or ^$)
    target: Redirect target URL, with replacement groups like $1, $2.
    perm: Create permanent (301) redirect, default is temporary (302).
    append_to: Append created redirect to list. If not specified, appends to
               module-level urlpatterns list.
    """

    # Patterns will be standard regex with e.g. (.*).
    # We need to convert these to valid Django pattern kwargs.
    # URLs have $1, $2.
    # We need to convert these to %(arg1)s, %(arg2)s.
    arg_count = 1
    url = target

    def convert_args(match):
        nonlocal arg_count, url

        # Ignore non-capturing groups.
        if match.group(0).startswith("?"):
            return match.group(0)

        url = url.replace(f"${arg_count}", f"%(arg{arg_count})s")

        group_with_arg = f"(?P<arg{arg_count}>{match.group(1)})"
        arg_count += 1
        return group_with_arg

    pattern = re.sub(r"\((?!\?)(.*?)\)", convert_args, pattern)

    urlpattern = re_path(
        f"^{pattern}$",
        RedirectView.as_view(url=url, permanent=permanent),
    )

    if append_to is None:
        append_to = urlpatterns

    append_to.append(urlpattern)

    return urlpattern


perm = partial(make_redirect, permanent=True)
temp = partial(make_redirect, permanent=False)


# Import redirects to populate urlpatterns.
from . import redirects  # noqa: E402, F401, I001
