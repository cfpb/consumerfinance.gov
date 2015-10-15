from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from wagtail.wagtailcore.templatetags import wagtailcore_tags

from jinja2 import Environment
from sheerlike import environment as sheerlike_environment
from compressor.contrib.jinja2ext import CompressorExtension


def environment(**options):
    options.setdefault('extensions', []).append(CompressorExtension)
    env = sheerlike_environment(**options)
    env.autoescape = False
    env.globals.update({
        'static': staticfiles_storage.url,
        'reverse': reverse,
    })
    env.filters.update({
        'slugify': slugify,
        'richtext': wagtailcore_tags.richtext
    })
    return env
