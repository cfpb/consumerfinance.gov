from __future__ import absolute_import
import os, re, HTMLParser
from urlparse import urlparse

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template.defaultfilters import pluralize, slugify, linebreaksbr
from wagtail.wagtailcore.templatetags import wagtailcore_tags
from django.contrib import messages

from jinja2 import Environment, contextfunction, Markup
from sheerlike import environment as sheerlike_environment
from compressor.contrib.jinja2ext import CompressorExtension
from flags.template_functions import flag_enabled, flag_disabled
from .util.util import get_unique_id, get_secondary_nav_items

from wagtail.wagtailcore.rich_text import expand_db_html, RichText
from bs4 import BeautifulSoup, NavigableString
from django.conf import settings
from processors.processors_common import fix_link

default_app_config = 'v1.apps.V1AppConfig'

def environment(**options):
    options.setdefault('extensions', []).append(CompressorExtension)
    options['extensions'].append('jinja2.ext.loopcontrols')
    env = sheerlike_environment(**options)
    env.autoescape = True
    from v1.models import CFGOVPage
    from v1.templatetags import share
    from v1.util import ref
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
        'get_page_state_url': share.get_page_state_url,
        'parse_links': parse_links,
        'get_protected_url': get_protected_url,
        'related_metadata_tags': related_metadata_tags,
        'get_filter_data': get_filter_data,
        'cfgovpage_objects': CFGOVPage.objects,
    })

    env.filters.update({
        'linebreaksbr': linebreaksbr,
        'pluralize': pluralize,
        'slugify': slugify
    })
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
        except:
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
EXTERNAL_A_CSS = os.environ.get('EXTERNAL_A_CSS', 'icon-link icon-link__external-link')
DOWNLOAD_A_CSS = os.environ.get('DOWNLOAD_A_CSS', 'icon-link icon-link__download')
EXTERNAL_SPAN_CSS = os.environ.get('EXTERNAL_SPAN_CSS', 'icon-link_text')


def add_link_markup(tags):
    for tag in tags:
        added_icon = False
        if not tag.attrs.get('class', None):
            tag.attrs.update({'class': []})
        if NONCFPB_LINK_PATTERN.match(tag['href']):
            # Sets the icon to indicate you're leaving consumerfinance.gov
            tag.attrs['class'].append(EXTERNAL_A_CSS)
            if EXTERNAL_LINK_PATTERN.match(tag['href']):
                # Sets the link to an external one if you're leaving .gov
                tag['href'] = '/external-site/?ext_url=' + tag['href']
            added_icon = True
        elif DOWNLOAD_LINK_PATTERN.search(tag['href']):
            # Sets the icon to indicate you're downloading a file
            tag.attrs['class'].append(DOWNLOAD_A_CSS)
            added_icon = True
        if added_icon:
            # Wraps the link text in a span that provides the underline
            contents = tag.contents
            span = BeautifulSoup('').new_tag('span')
            span['class'] = EXTERNAL_SPAN_CSS
            span.contents = contents
            tag.contents = [span, NavigableString(' ')]
        elif not FILES_LINK_PATTERN.match(tag['href']):
            fix_link(tag)


@contextfunction
def render_stream_child(context, stream_child):
    # Use the django_jinja to get the template content based on its name
    try:
        template = context.environment.get_template(stream_child.block.meta.template)
    except:
        return stream_child

    # Create a new context based on the current one as we can't edit it directly
    new_context = context.get_all()
    # Add the value on the context (value is the keyword chosen by wagtail for the blocks context)
    try:
        new_context['value'] = stream_child.value
    except:
        new_context['value'] = stream_child

    # Render the template with the context
    html = template.render(new_context)
    unescaped = HTMLParser.HTMLParser().unescape(html)
    # Return the rendered template as safe html
    return Markup(unescaped)


@contextfunction
def get_protected_url(context, page):
    if page is None:
        return '#'

    request_hostname = urlparse(context['request'].url).hostname
    url = page.url
    if url is None:  # If page is not aligned to a site root return None
        return None
    page_hostname = urlparse(url).hostname
    staging_hostname = os.environ.get('DJANGO_STAGING_HOSTNAME')
    if page.live:
        return url
    elif page.specific.shared:
        if request_hostname == staging_hostname:
            return url.replace(page_hostname, staging_hostname)
        else:
            return '#'


@contextfunction
def related_metadata_tags(context, page):
    request = context['request']
    # Set the tags to correct data format
    tags = {'links': []}
    # From an ancestor, get the form ids then use the first id since the
    # filterable list on the page will probably have the first id on the page.
    id, filter_page = get_filter_data(page)
    for tag in page.specific.tags.names():
        tag_link = {'text': tag, 'url': ''}
        if id is not None and filter_page is not None:
            param = '?filter' + str(id) + '_topics=' + tag
            tag_link['url'] = get_protected_url(context, filter_page) + param
        tags['links'].append(tag_link)
    return tags


def get_filter_data(page):
    for ancestor in page.get_ancestors().reverse().specific():
        if ancestor.specific_class.__name__ in ['BrowseFilterablePage', 'SublandingFilterablePage',
                                                'EventArchivePage', 'NewsroomLandingPage']:
            return util.get_form_id(ancestor), ancestor
    return None, None
