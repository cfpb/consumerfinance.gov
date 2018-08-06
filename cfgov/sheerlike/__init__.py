# Python 2 only
from __future__ import absolute_import

import os
import os.path

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse

import jinja2.runtime
from jinja2 import Environment
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


class SheerlikeEnvironment(Environment):

    def join_path(self, template, parent):
        dirname = os.path.dirname(parent)
        segments = dirname.split('/')
        paths = []
        collected = ''
        for segment in segments:
            collected += segment + '/'
            paths.insert(0, collected[:])
        for p in paths:
            relativepath = os.path.join(p, template)
            for search in self.loader.searchpath:
                filesystem_path = os.path.join(search, relativepath)
                if os.path.exists(filesystem_path):
                    return relativepath
        return template


def environment(**options):
    options.setdefault('extensions', []).append('jinja2.ext.do')

    env = SheerlikeEnvironment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'when': when,
    })
    env.filters.update({
        'date': get_date_string,
        'dateobj': get_date_obj
    })
    return env
