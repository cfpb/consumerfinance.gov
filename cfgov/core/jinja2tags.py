from django.utils import translation

from jinja2 import pass_context
from jinja2.ext import Extension, nodes

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
                "slugify_unique": pass_context(slugify_unique),
            }
        )


class LanguageExtension(Extension):
    """Jinja extension used to translate text into a specific language.

    For example:

    {% language "es" %}{{ _( 'Spanish' ) }}{% endlanguage %}

    This will render "Español".

    Based off of the Django {% language %} tag documented at:

    https://docs.djangoproject.com/en/stable/topics/i18n/translation/#switching-language-in-templates
    """

    tags = {"language"}

    def parse(self, parser):
        # Line number of the {% language %} tag.
        lineno = next(parser.stream).lineno

        # Parse the language code argument, e.g. "es" from {% language "es" %}.
        args = [parser.parse_expression()]

        # Parse the content up to and including the {% endlanguage %} tag.
        body = parser.parse_statements(["name:endlanguage"], drop_needle=True)

        # Return the node that will activate the specified language
        # before rendering the parsed content.
        return nodes.CallBlock(
            self.call_method("activate_language", args), [], [], body
        ).set_lineno(lineno)

    def activate_language(self, language_code, caller):
        with translation.override(language_code):
            return caller()


filters = CoreExtension
language = LanguageExtension
