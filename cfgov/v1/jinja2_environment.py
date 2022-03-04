import os.path

from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaultfilters import linebreaksbr, pluralize, slugify
from django.urls import reverse
from django.utils.translation import gettext, ngettext

from jinja2 import Environment

from search.models import AUTOCOMPLETE_MAX_CHARS


class RelativeTemplatePathEnvironment(Environment):
    """Jinja2 environment that supports template loading with relative paths.

    By default, Jinja2 (and Django) template loading works with "absolute"
    paths relative to the root template directories specified in Django
    settings. Consider, for example, if the root template directories include
    a directory like /foo, and within that directory there exists some
    template /foo/bar/template.html, and that template includes this
    directive:

    {% include "other_template.html" %}

    by default, the template loader will look to load that template relative
    to the root template directories. In this case, it would look to load
    the template /foo/other_template.html.

    This custom Jinja2 environment class modifies that behavior to also
    support relative template loading, which would make the search path look
    like this instead:

    /foo/bar/other_template.html
    /foo/other_template.html

    This logic adds relative paths to the template search tree, that take
    precendence over the default loader source directories.
    """

    def join_path(self, template, parent):
        dirname = os.path.dirname(parent)
        segments = dirname.split("/")
        paths = []
        collected = ""
        for segment in segments:
            collected += segment + "/"
            paths.insert(0, collected[:])
        for p in paths:
            relativepath = os.path.join(p, template)
            for search in self.loader.searchpath:
                filesystem_path = os.path.join(search, relativepath)
                if os.path.exists(filesystem_path):
                    return relativepath
        return template


class JinjaTranslations:
    def gettext(self, message):
        return gettext(message)

    def ngettext(self, singular, plural, number):
        return ngettext(singular, plural, number)


def environment(**options):
    # If running Django in debug mode, enable the Jinja2 {% debug %} tag.
    # We do this here instead of in settings because DEBUG's value may be
    # not be set until after the default Jinja configuration is defined.
    #
    # https://jinja.palletsprojects.com/en/2.11.x/extensions/#debug-extension
    #
    # Use of the {% debug %} tag when this extension isn't installed (when
    # DEBUG is False) will trigger a 500 error with a
    # jinja2.exceptions.TemplateSyntaxError. In theory we should never be using
    # this tag for pages in production, but, if we did, we wouldn't want to
    # accidentally expose debug information, so this seems like sensible
    # behavior.
    #
    # It might be better if {% debug %} would instead work as a no-op and print
    # nothing in the DEBUG=False case, but that would require writing our own
    # custom tag. Relatedly, the Django template language's {% debug %} tag is
    # always defined and always renders debug information regardless of the
    # value of settings.DEBUG:
    #
    # https://docs.djangoproject.com/en/2.2/ref/templates/builtins/#debug
    if settings.DEBUG:
        extensions = options.setdefault("extensions", [])
        debug_extension = "jinja2.ext.debug"
        if debug_extension not in extensions:
            extensions.append(debug_extension)

    env = RelativeTemplatePathEnvironment(**options)
    env.autoescape = True

    # Requires the jinja2.ext.i18n extension.
    env.install_gettext_translations(JinjaTranslations(), newstyle=True)

    # Expose various Django methods into the Jinja2 environment.
    env.globals.update(
        {
            "autocomplete_max_chars": AUTOCOMPLETE_MAX_CHARS,
            "get_messages": messages.get_messages,
            "reverse": reverse,
            "static": staticfiles_storage.url,
            "url": reverse,
        }
    )

    env.filters.update(
        {
            "linebreaksbr": linebreaksbr,
            "pluralize": pluralize,
            "slugify": slugify,
        }
    )

    return env
