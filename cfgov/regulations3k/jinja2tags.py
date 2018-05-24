
from wagtail.contrib.wagtailroutablepage.templatetags.wagtailroutablepage_tags import (  # noqa: E501
    routablepageurl
)

import jinja2
from jinja2.ext import Extension
from jinja2.filters import do_mark_safe
from regulations3k.regdown import regdown as regdown_func


def regdown_filter(text):
    return do_mark_safe(regdown_func(text))


class RegulationsExtension(Extension):

    def __init__(self, environment):
        super(RegulationsExtension, self).__init__(environment)

        self.environment.globals.update({
            'routablepageurl': jinja2.contextfunction(routablepageurl),
        })
        self.environment.filters.update({
            'regdown': regdown_filter,
        })


regulations = RegulationsExtension
