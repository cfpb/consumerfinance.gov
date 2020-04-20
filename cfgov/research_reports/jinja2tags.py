import html

from jinja2 import Markup
from jinja2.ext import Extension


def render_rich_html(parsed_html):
    unescaped = html.unescape(parsed_html)
    # Return the rendered template as safe html
    return Markup(unescaped)


class ResearchReportsExtension(Extension):
    def __init__(self, environment):
        super(ResearchReportsExtension, self).__init__(environment)
        self.environment.globals.update({
            'render_rich_html': render_rich_html,
        })
