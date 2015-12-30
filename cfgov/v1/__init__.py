from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from wagtail.wagtailcore.templatetags import wagtailcore_tags
from django.contrib import messages

import HTMLParser
from jinja2 import Environment, contextfunction, Markup
from sheerlike import environment as sheerlike_environment
from compressor.contrib.jinja2ext import CompressorExtension
from flags.template_functions import flag_enabled, flag_disabled

def environment(**options):
    options.setdefault('extensions', []).append(CompressorExtension)
    env = sheerlike_environment(**options)
    env.autoescape = True
    from v1.models import CFGOVPage
    env.globals.update({
        'static': staticfiles_storage.url,
        'global_dict': {
            'related_posts_function': lambda x: {
                'posts': CFGOVPage.objects.all()[:x['value']['limit']],
                'newsroom': CFGOVPage.objects.all()[:x['value']['limit']],
                'events': CFGOVPage.objects.all()[:x['value']['limit']]
            }
        },
        'reverse': reverse,
        'render_stream_child': render_stream_child,
        'flag_enabled': flag_enabled,
        'flag_disabled': flag_disabled,
        'get_unique_id': get_unique_id,
        'get_messages': messages.get_messages
    })
    env.filters.update({
        'slugify': slugify,
    })
    return env

@contextfunction
def get_unique_id(context, prefix='', suffix=''):
    if hasattr(context, 'unique_id_index'):
        context.unique_id_index += 1
    else:
        context.unique_id_index = 0
    return prefix + str(context.unique_id_index) + suffix

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
