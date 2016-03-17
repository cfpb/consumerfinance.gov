import os, re,HTMLParser

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from wagtail.wagtailcore.templatetags import wagtailcore_tags
from django.contrib import messages

from jinja2 import Environment, contextfunction, Markup
from sheerlike import environment as sheerlike_environment
from compressor.contrib.jinja2ext import CompressorExtension
from flags.template_functions import flag_enabled, flag_disabled
from util.util import get_unique_id

from wagtail.wagtailcore.rich_text import expand_db_html
from BeautifulSoup import BeautifulSoup

default_app_config = 'v1.apps.V1AppConfig'

def environment(**options):
    options.setdefault('extensions', []).append(CompressorExtension)
    options['extensions'].append('jinja2.ext.loopcontrols')
    env = sheerlike_environment(**options)
    env.autoescape = True
    from v1.models import ref, CFGOVPage
    from v1.templatetags import share
    env.globals.update({
        'static': staticfiles_storage.url,
        'global_dict': {
        },
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
        'get_page_state_url': share.get_page_state_url,
        'cfgov_rich_text': external_links,
    })
    env.filters.update({
        'slugify': slugify,
    })
    return env

EXTERNAL_LINK_PATTERN = '(https?:\/\/(?:www\.)?(?![^\?]*(cfpb|consumerfinance).gov)(?!(content\.)?localhost).*)'


def external_links(value):
    soup = BeautifulSoup(expand_db_html(value.source))

    try:
        p = re.compile(EXTERNAL_LINK_PATTERN)

        for a in soup('a'):
            if p.match(a['href']):
                a['class'] = os.environ.get('EXTERNAL_LINK_CSS', 'icon-link icon-link__external-link')
    except:
        pass

    return soup


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
    new_context['value'] = stream_child.value
    # Render the template with the context
    html = template.render(new_context)
    unescaped = HTMLParser.HTMLParser().unescape(html)
    # Return the rendered template as safe html
    return Markup(unescaped)
