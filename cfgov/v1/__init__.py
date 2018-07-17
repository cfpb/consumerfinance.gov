from __future__ import absolute_import

import unicodedata
from six import text_type as unicode
from six.moves import html_parser as HTMLParser

from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import caches
from django.core.urlresolvers import reverse
from django.template.defaultfilters import linebreaksbr, pluralize, slugify
from django.utils.module_loading import import_string
from django.utils.timezone import template_localtime
from django.utils.translation import ugettext, ungettext

from flags.template_functions import flag_disabled, flag_enabled
from jinja2 import Markup, contextfunction

from core.utils import signed_redirect, unsigned_redirect
from sheerlike import environment as sheerlike_environment
from v1.fragment_cache_extension import FragmentCacheExtension
from v1.routing import get_protected_url
from v1.util.util import get_unique_id


default_app_config = 'v1.apps.V1AppConfig'


class JinjaTranslations(object):

    def gettext(self, message):
        return ugettext(message)

    def ngettext(self, singular, plural, number):
        return ungettext(singular, plural, number)


def strip_accents(value):
    nfkd_form = unicodedata.normalize('NFKD', unicode(value))
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def environment(**options):
    from v1.models import CFGOVPage
    from v1.templatetags.activity_feed import get_latest_activities
    from v1.templatetags.mega_menu import get_menu_items
    from v1.util import ref

    options.setdefault('extensions', [])
    options['extensions'].append('jinja2.ext.loopcontrols')
    options['extensions'].append('jinja2.ext.i18n')
    options['extensions'].append(FragmentCacheExtension)
    env = sheerlike_environment(**options)
    env.autoescape = True
    env.install_gettext_translations(JinjaTranslations())
    env.globals.update({
        'static': staticfiles_storage.url,
        'global_dict': {},
        'reverse': reverse,
        'render_stream_child': render_stream_child,
        'flag_enabled': flag_enabled,
        'flag_disabled': flag_disabled,
        'get_unique_id': get_unique_id,
        'get_messages': messages.get_messages,
        'category_label': ref.category_label,
        'fcm_label': ref.fcm_label,
        'choices_for_page_type': ref.choices_for_page_type,
        'is_blog': ref.is_blog,
        'is_report': ref.is_report,
        'cfgovpage_objects': CFGOVPage.objects,
        'signed_redirect': signed_redirect,
        'unsigned_redirect': unsigned_redirect,
        'get_protected_url': get_protected_url,
        'get_latest_activities': get_latest_activities,
        'get_menu_items': get_menu_items,
        'get_snippets': get_snippets,
        'localtime': template_localtime,
        'strip_accents': strip_accents,
    })

    env.filters.update({
        'linebreaksbr': linebreaksbr,
        'localtime': template_localtime,
        'pluralize': pluralize,
        'slugify': slugify,
    })
    env.fragment_cache = caches['post_preview']
    return env


@contextfunction
def render_stream_child(context, stream_child):
    # Use the django_jinja to get the template content based on its name
    try:
        template = context.environment.get_template(
            stream_child.block.meta.template)
    except Exception:
        return stream_child

    # Create a new context based on the current one as we can't edit it
    # directly
    new_context = context.get_all()
    # Add the value on the context (value is the keyword chosen by
    # wagtail for the blocks context)
    try:
        new_context['value'] = stream_child.value
    except AttributeError:
        new_context['value'] = stream_child

    # Render the template with the context
    html = template.render(new_context)
    unescaped = HTMLParser.HTMLParser().unescape(html)
    # Return the rendered template as safe html
    return Markup(unescaped)


def get_snippets(snippet_type):
    snippet_class = import_string(snippet_type)
    return snippet_class
