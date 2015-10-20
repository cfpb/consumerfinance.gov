from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from wagtail.wagtailcore.templatetags import wagtailcore_tags

import jinja2
from sheerlike import environment as sheerlike_environment
from compressor.contrib.jinja2ext import CompressorExtension


def environment(**options):
    options.setdefault('extensions', []).append(CompressorExtension)
    env = sheerlike_environment(**options)
    env.autoescape = True
    env.globals.update({
        'static': staticfiles_storage.url,
        'reverse': reverse
    })
    env.filters.update({
        'slugify': slugify
    })
    return env
