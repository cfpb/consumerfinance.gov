from flags.template_functions import flag_disabled, flag_enabled
from jinja2.ext import Extension

from core.templatetags.svg_icon import svg_icon


class CoreExtension(Extension):
    def __init__(self, environment):
        super(CoreExtension, self).__init__(environment)
        self.environment.globals.update({
            'flag_enabled': flag_enabled,
            'flag_disabled': flag_disabled,

            'svg_icon': svg_icon,
        })


filters = CoreExtension
