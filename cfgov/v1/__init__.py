from __future__ import absolute_import

import os
import re
import unicodedata
from six import text_type as unicode
from six.moves import html_parser as HTMLParser
from six.moves.urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import caches
from django.core.urlresolvers import reverse
from django.template.defaultfilters import linebreaksbr, pluralize, slugify
from django.utils.module_loading import import_string
from django.utils.timezone import template_localtime
from django.utils.translation import ugettext, ungettext

from wagtail.wagtailcore.rich_text import RichText, expand_db_html

from bs4 import BeautifulSoup, NavigableString
from flags.template_functions import flag_disabled, flag_enabled
from jinja2 import Markup, contextfunction

from core.templatetags.svg_icon import svg_icon
from core.utils import signed_redirect, unsigned_redirect
from processors.processors_common import fix_link
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
        'parse_links': parse_links,
        'cfgovpage_objects': CFGOVPage.objects,
        'signed_redirect': signed_redirect,
        'unsigned_redirect': unsigned_redirect,
        'get_protected_url': get_protected_url,
        'get_latest_activities': get_latest_activities,
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


def parse_links(value):
    if isinstance(value, RichText):
        soup = BeautifulSoup(expand_db_html(value.source), 'html.parser')
    else:
        soup = BeautifulSoup(expand_db_html(value), 'html.parser')

    # This removes style tags <style>
    for s in soup('style'):
        s.decompose()

    # This removes all inline style attr's
    for tag in soup.recursiveChildGenerator():
        try:
            del tag['style']
        except TypeError:
            # 'NavigableString' object has does not have attr's
            pass

    # This adds the link markup
    link_tags = get_link_tags(soup)
    add_link_markup(link_tags)

    return soup


def get_link_tags(soup):
    tags = []
    for a in soup.find_all('a', href=True):
        if not is_image_tag(a):
            tags.append(a)
    return tags


def is_image_tag(tag):
    for child in tag.children:
        if child.name in ['img', 'svg']:
            return True
    return False


EXTERNAL_LINK_PATTERN = re.compile(settings.EXTERNAL_LINK_PATTERN)
NONCFPB_LINK_PATTERN = re.compile(settings.NONCFPB_LINK_PATTERN)
FILES_LINK_PATTERN = re.compile(settings.FILES_LINK_PATTERN)
DOWNLOAD_LINK_PATTERN = re.compile(settings.DOWNLOAD_LINK_PATTERN)
LINK_ICON_CLASSES = os.environ.get('LINK_ICON_CLASSES',
                                   'a-link a-link__icon')
LINK_ICON_TEXT_CLASSES = os.environ.get('LINK_ICON_TEXT_CLASSES',
                                        'a-link_text')


def add_link_markup(tags):

    for tag in tags:
        icon = False
        if not tag.attrs.get('class', None):
            tag.attrs.update({'class': []})
        if tag['href'].startswith('/external-site/?'):
            components = urlparse(tag['href'])
            arguments = parse_qs(components.query)
            if 'ext_url' in arguments:
                external_url = arguments['ext_url'][0]
                tag['href'] = signed_redirect(external_url)

        elif NONCFPB_LINK_PATTERN.match(tag['href']):
            # Sets the icon to indicate you're leaving consumerfinance.gov
            tag.attrs['class'].append(LINK_ICON_CLASSES)

            if EXTERNAL_LINK_PATTERN.match(tag['href']):
                tag['href'] = signed_redirect(tag['href'])

            icon = 'external-link'
        elif DOWNLOAD_LINK_PATTERN.search(tag['href']):
            # Sets the icon to indicate you're downloading a file
            tag.attrs['class'].append(LINK_ICON_CLASSES)
            icon = 'download'
        if icon:
            # Wraps the link text in a span that provides the underline
            contents = tag.contents
            span = BeautifulSoup('', 'html.parser').new_tag('span')
            span['class'] = LINK_ICON_TEXT_CLASSES
            span.contents = contents
            tag.contents = [span, NavigableString(' ')]
            # Appends the SVG icon
            tag.contents.append(BeautifulSoup(svg_icon(icon), 'html.parser'))
        elif not FILES_LINK_PATTERN.match(tag['href']):
            fix_link(tag)


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
