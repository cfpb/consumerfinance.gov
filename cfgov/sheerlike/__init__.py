# Python 2 only
from __future__ import absolute_import

import jinja2.runtime
from jinja2.runtime import Context

from .middleware import get_request


default_app_config = 'sheerlike.apps.SheerlikeConfig'


class SheerlikeContext(Context):

    def __init__(self, environment, parent, name, blocks):
        super(
            SheerlikeContext,
            self).__init__(
            environment,
            parent,
            name,
            blocks)

        # Don't overwrite an existing request already coming into the context,
        # for example one provided during Wagtail rendering.
        if 'request' not in self.vars and 'request' not in self.keys():
            try:
                self.vars['request'] = get_request()
            except Exception:
                pass


# Monkey patch not needed in master version of Jinja2
# https://github.com/mitsuhiko/jinja2/commit/f22fdd5ffe81aab743f78290071b0aa506705533
jinja2.runtime.Context = SheerlikeContext
