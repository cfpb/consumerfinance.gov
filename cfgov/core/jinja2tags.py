from jinja2.ext import Extension

from core.templatetags.svg_icon import svg_icon
from core.utils import signed_redirect, unsigned_redirect


class CoreExtension(Extension):
    def __init__(self, environment):
        super(CoreExtension, self).__init__(environment)
        self.environment.globals.update({
            'signed_redirect': signed_redirect,
            'unsigned_redirect': unsigned_redirect,

            'svg_icon': svg_icon,
        })


filters = CoreExtension
