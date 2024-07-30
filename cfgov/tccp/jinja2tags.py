import re
from urllib.parse import urlparse

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


# Contact website schemes must be either http or https.
_valid_website_scheme = re.compile(r"https?")


# Contact website hosts must have at least one . in them.
_valid_website_netloc = re.compile(r".+\..+")


# We strip www. from the beginning of displayed URLs.
_leading_www = re.compile(r"^www\.")


def _format_contact_website(url):
    parsed_url = urlparse(url)

    if _valid_website_scheme.match(
        parsed_url.scheme or ""
    ) and _valid_website_netloc.match(parsed_url.netloc or ""):
        return {"url": url, "text": _leading_www.sub("", parsed_url.netloc)}
    else:
        return {
            "text": url,
        }


def _format_contact_phone_number(phone_number):
    phone_number = "".join(
        c for c in phone_number if c.isalpha() or c.isdigit()
    )
    return phone_number[phone_number.startswith("1") :]


def _format_contact_info(card):
    def fmt_list(format_fn, value):
        return list(map(format_fn, (value or "").split()))

    return {
        "urls": fmt_list(
            _format_contact_website, card["website_for_consumer"]
        ),
        "phone_number": _format_contact_phone_number(
            card["telephone_number_for_consumers"] or ""
        ),
    }


def render_contact_info(card):
    return mark_safe(
        render_to_string(
            "tccp/includes/contact_info.html",
            _format_contact_info(card),
        )
    )
