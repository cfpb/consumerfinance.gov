from __future__ import absolute_import  # Python 2 only

import os
import os.path
import functools
import warnings

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.conf import settings

from jinja2 import Environment
import jinja2.runtime
from jinja2.runtime import Context

from unipath import Path

from .query import QueryFinder, more_like_this, get_document, when
from .filters import selected_filters_for_field, is_filter_selected
from .templates import date_formatter
from .middleware import get_request

PERMALINK_REGISTRY={}

def register_permalink(sheer_type, url_pattern_name):
    PERMALINK_REGISTRY[sheer_type]=url_pattern_name

def url_for(app, filename):
    if app == 'static':
        return staticfiles_storage.url(filename)
    else:
        raise ValueError("url_for doesn't know about %s" % app)

class SheerlikeContext(Context):
    def __init__(self, environment, parent, name, blocks):
        super(SheerlikeContext, self).__init__(environment, parent, name, blocks)
        try:
            self.vars['request'] = get_request()
        except:
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
            paths.insert(0,collected[:])
        for p in paths:
            relativepath = os.path.join(p, template)
            for search in self.loader.searchpath:
                filesystem_path = os.path.join(search, relativepath)
                if os.path.exists(filesystem_path):
                    return relativepath
        return template

def environment(**options):
    queryfinder = QueryFinder()

    searchpath =[]
    staticdirs = []

    sites = settings.SHEER_SITES
    for site in sites:
        site_path = Path(site)
        searchpath.append(site_path)
        searchpath.append(site_path.child('_includes'))
        searchpath.append(site_path.child('_layouts'))
        staticdirs.append(site_path.child('static'))

    options['loader'].searchpath += searchpath
    settings.STATICFILES_DIRS += staticdirs

    options.setdefault('extensions', []).append('jinja2.ext.do')

    env = SheerlikeEnvironment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url_for': url_for,
        'url': reverse,
        'queries': queryfinder,
        'more_like_this': more_like_this,
        'get_document': get_document,
        'selected_filters_for_field': selected_filters_for_field,
        'is_filter_selected': is_filter_selected,
        'when': when
    })
    env.filters.update({
        'date': date_formatter
    })
    return env
