# This command overrides the built-in Django makemessages command to extract
# messages from both Django templates and Jinja2 templates.
#
# The code is based on this StackOverflow question and answer:
# https://stackoverflow.com/questions/2090717/getting-translation-strings-for-jinja2-templates-integrated-with-django-1-x
# And the Django docs:
# https://docs.djangoproject.com/en/stable/topics/i18n/translation/#customizing-the-makemessages-command

import re

from django.core.management.commands import makemessages
from django.utils.translation import template as translate_tag


class Command(makemessages.Command):
    def handle(self, *args, **options):
        # Jinja2 uses {% trans %}…{% endtrans %}
        jinja_block_re = re.compile(r"^\s*trans(?:\s+|$)")
        jinja_endblock_re = re.compile(r"^\s*endtrans$")

        # Django uses {% blocktranslate %}…{% endblocktranslate %}
        django_block_re = translate_tag.block_re
        django_endblock_re = translate_tag.endblock_re

        # This monkey-patches support for Jinja2's:
        # {% translate %}{% endtrans %}
        # blocks into trans_real's block/endblock-matching regular expressions.
        # These differ from Django's
        # {% blocktranslate %}{% endblocktranslate %}
        # blocks.
        #
        # trans_real's other regular expressions, context_re, inline_re,
        # plural_re, constant_re, and one_percent_re should match both Jinja2
        # and Django conventions.
        translate_tag.block_re = re.compile(
            django_block_re.pattern + "|" + jinja_block_re.pattern
        )
        translate_tag.endblock_re = re.compile(
            django_endblock_re.pattern + "|" + jinja_endblock_re.pattern
        )

        # The rest of trans_real's regular expressions should match conventions
        # used in both Django and Jinja2 templates.
        # Call makemessages
        super().handle(*args, **options)

        # Restore just the Django-matching regular expressions
        translate_tag.endblock_re = django_endblock_re
        translate_tag.block_re = django_block_re
