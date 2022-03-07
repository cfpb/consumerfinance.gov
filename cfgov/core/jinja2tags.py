from jinja2 import contextfilter
from jinja2.ext import Extension

from core.templatetags.richtext import richtext_isempty
from core.templatetags.svg_icon import svg_icon
from core.utils import slugify_unique


class CoreExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        self.environment.globals.update(
            {
                "svg_icon": svg_icon,
            }
        )

        self.environment.filters.update(
            {
                "richtext_isempty": richtext_isempty,
                "slugify_unique": contextfilter(slugify_unique),
            }
        )


filters = CoreExtension
