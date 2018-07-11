# Python 2 only
from __future__ import absolute_import

import os
import os.path

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse

from flags.template_functions import flag_disabled, flag_enabled
from jinja2 import Environment

from .query import QueryFinder, get_document, more_like_this, when
from .templates import get_date_obj, get_date_string


default_app_config = 'sheerlike.apps.SheerlikeConfig'


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
    queryfinder = QueryFinder()

    options.setdefault('extensions', []).append('jinja2.ext.do')

    env = SheerlikeEnvironment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'queries': queryfinder,
        'more_like_this': more_like_this,
        'get_document': get_document,
        'when': when,
        'flag_enabled': flag_enabled,
        'flag_disabled': flag_disabled,
    })
    env.filters.update({
        'date': get_date_string,
        'dateobj': get_date_obj
    })
    return env
