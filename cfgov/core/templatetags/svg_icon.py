import logging
import re

from django import template
from django.contrib.staticfiles import finders
from django.utils.safestring import SafeString, mark_safe


logger = logging.getLogger(__name__)
register = template.Library()


FALLBACK_ICON_NAME = "error"
SVG_REGEX = re.compile(
    r"^"  # start of string
    r"\s*"  # any leading whitespace
    r"<svg[^>]*>"  # opening <svg> tag with any attributes
    r"(?!.*</svg>.*</svg>)"  # only allow one closing </svg> tag
    r".*</svg>"  # match anything and then the closing tag
    r"\s*"  # any trailing whitespace
    r"$",  # end of string
    re.DOTALL | re.IGNORECASE | re.MULTILINE,
)


def load_svg(name: str, attrs: dict) -> str:
    relative_path = f"icons/{name}.svg"
    if not (static_filename := finders.find(relative_path)):
        raise FileNotFoundError(f"{relative_path} not found in staticfiles.")

    with open(static_filename, "r") as f:
        content = f.read()
        if not SVG_REGEX.match(content):
            raise ValueError(f"{static_filename} not a valid SVG.")
        if attrs:
            attrs = " ".join([f"{key}='{value}'" for key, value in attrs.items()])
            content = content.replace("<svg", f"<svg {attrs}")
    return content


@register.simple_tag()
def svg_icon(name: str, attrs: dict = {}) -> SafeString:
    """Return SVG content given an icon name."""
    try:
        content = load_svg(name, attrs)
    except (FileNotFoundError, ValueError) as e:
        logger.warning(f"{e} Substituting with {FALLBACK_ICON_NAME}.svg!")
        content = load_svg(FALLBACK_ICON_NAME, attrs)
    return mark_safe(content)
