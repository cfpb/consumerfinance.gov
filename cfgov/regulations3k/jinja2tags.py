import datetime

from wagtail.contrib.routable_page.templatetags.wagtailroutablepage_tags import (  # noqa: B950
    routablepageurl,
)

import jinja2
from dateutil import parser
from jinja2.ext import Extension
from jinja2.filters import do_mark_safe
from regdown import regdown as regdown_func


def ap_date(date):
    """Convert a date object or date string into an AP-styled date string."""
    if date is None:
        return None
    if type(date) != datetime.date:
        try:
            date = parser.parse(date).date()
        except ValueError:
            return
    if date.month in [3, 4, 5, 6, 7]:
        return date.strftime("%B {}, %Y").format(date.day)
    elif date.month == 9:
        return date.strftime("Sept. {}, %Y").format(date.day)
    else:
        return date.strftime("%b. {}, %Y").format(date.day)


def regdown_filter(text):
    return do_mark_safe(regdown_func(text))


def regs_hide_on_mobile(text):
    """Mark specific patterns in text as hidden on mobile"""
    text = do_mark_safe(
        text.replace("Regulation", 'Reg<span class="u-hide-on-mobile">ulation</span>')
    )
    return text


class RegulationsExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)

        self.environment.globals.update(
            {
                "routablepageurl": jinja2.contextfunction(routablepageurl),
                "ap_date": ap_date,
            }
        )
        self.environment.filters.update(
            {
                "regdown": regdown_filter,
                "regs_hide_on_mobile": regs_hide_on_mobile,
            }
        )


regulations = RegulationsExtension
