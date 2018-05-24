import re

from django import template
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe


register = template.Library()


SVG_REGEX = re.compile(
    r'^'                    # start of string
    '\s*'                   # any leading whitespace
    '<svg[^>]*>'            # opening <svg> tag with any attributes
    '(?!.*</svg>.*</svg>)'  # only allow one closing </svg> tag
    '.*</svg>'              # match anything and then the closing tag
    '\s*'                   # any trailing whitespace
    '$',                    # end of string
    re.DOTALL | re.IGNORECASE | re.MULTILINE
)


@register.simple_tag()
def svg_icon(name):
    """Return SVG content given an icon name."""
    relative_path = 'icons/{}.svg'.format(name)
    static_filename = finders.find(relative_path)

    if not static_filename:
        raise ValueError('{} not found in staticfiles'.format(relative_path))

    with open(static_filename, 'r') as f:
        content = f.read()

        if not SVG_REGEX.match(content):
            raise ValueError('{} is not a valid SVG'.format(static_filename))

        return mark_safe(content)
