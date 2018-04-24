from jinja2.ext import Extension
from jinja2.filters import do_mark_safe
from regulations3k.regdown import regdown as regdown_func


def regdown_filter(text):
    return do_mark_safe(regdown_func(text))


class RegDownExtension(Extension):

    def __init__(self, environment):
        super(RegDownExtension, self).__init__(environment)

        self.environment.filters.update({
            'regdown': regdown_filter,
        })


regdown = RegDownExtension
