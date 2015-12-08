from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from wagtail.wagtailcore.templatetags import wagtailcore_tags

import HTMLParser
from jinja2 import Environment, contextfunction, Markup
from sheerlike import environment as sheerlike_environment
from compressor.contrib.jinja2ext import CompressorExtension


def environment(**options):
    options.setdefault('extensions', []).append(CompressorExtension)
    env = sheerlike_environment(**options)
    env.autoescape = True
    env.globals.update({
        'static': staticfiles_storage.url,
        'global_dict': {},
        'reverse': reverse,
        'render_stream_child': render_stream_child
    })
    env.filters.update({
        'slugify': slugify,
        'richtext': wagtailcore_tags.richtext
    })
    return env


@contextfunction
def render_stream_child(context, stream_child):
    # Use the django_jinja to get the template content based on its name
    template = context.environment.get_template(stream_child.block.meta.template)
    # Create a new context based on the current one as we can't edit it directly
    new_context = context.get_all()
    # Add the value on the context (value is the keyword chosen by wagtail for the blocks context)
    new_context['value'] = stream_child.value
    # Render the template with the context
    html = template.render(new_context)
    unescaped = HTMLParser.HTMLParser().unescape(html)
    # Return the rendered template as safe html
    return Markup(unescaped)