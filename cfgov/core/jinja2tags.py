from jinja2.ext import Extension

from core.templatetags.svg_icon import svg_icon


class CoreExtension(Extension):
    def __init__(self, environment):
        super(CoreExtension, self).__init__(environment)
        self.environment.globals.update({
            'svg_icon': svg_icon,
        })


filters = CoreExtension
