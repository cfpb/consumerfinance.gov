# Python 2 only
from __future__ import absolute_import

import os
import os.path
import functools

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from django.utils.html import mark_safe

from jinja2 import Environment
import jinja2.runtime
from jinja2.runtime import Context

from .query import QueryFinder, more_like_this, get_document, when
from .filters import selected_filters_for_field, is_filter_selected
from .templates import get_date_string, get_date_obj
from .middleware import get_request


from flags.template_functions import flag_enabled, flag_disabled

default_app_config = 'sheerlike.apps.SheerlikeConfig'


def global_render_template(name, **kwargs):
    request = get_request()
    context = RequestContext(request, kwargs or None)
    context['request'] = request
    template = loader.get_template(name, using='wagtail-env')
    return mark_safe(template.render(context.flatten()))


def url_for(app, filename, site_slug=None):
    if app == 'static' and not site_slug:
        return staticfiles_storage.url(filename)
    elif app == 'static':
        return staticfiles_storage.url(site_slug + '/static/' + filename)
    else:
        raise ValueError("url_for doesn't know about %s" % app)


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

    site_slug = options.get('site_slug')
    if site_slug:
        del options['site_slug']
    env = SheerlikeEnvironment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url_for': functools.partial(url_for, site_slug=site_slug),
        'url': reverse,
        'queries': queryfinder,
        'more_like_this': more_like_this,
        'get_document': get_document,
        'selected_filters_for_field': selected_filters_for_field,
        'is_filter_selected': is_filter_selected,
        'when': when,
        'flag_enabled': flag_enabled,
        'flag_disabled': flag_disabled,
        'global_include': global_render_template,
    })
    env.filters.update({
        'date': get_date_string,
        'dateobj': get_date_obj
    })
    return env
