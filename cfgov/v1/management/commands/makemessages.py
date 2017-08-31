# -*- coding: utf-8 -*-
# This command overrides the built-in Django makemessages command to extract
# messages from both Django templates and Jinja2 templates.
#
# The code is based on this StackOverflow question and answer:
# https://stackoverflow.com/questions/2090717/getting-translation-strings-for-jinja2-templates-integrated-with-django-1-x
# And the Django docs:
# https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#customizing-the-makemessages-command

import re

from django import VERSION
from django.core.management.commands import makemessages

if VERSION[:2] < (1, 11):
    from django.utils.translation import trans_real
else:
    from django.utils.translation import template as trans_real


class Command(makemessages.Command):

    def handle(self, *args, **options):
        # Jinja2 uses {% trans %}…{% endtrans %}
        jinja_block_re = re.compile(r'^\s*trans(?:\s+|$)')
        jinja_endblock_re = re.compile(r'^\s*endtrans$')

        # Django uses {% blocktrans %}…{% endblocktrans %}
        django_block_re = trans_real.block_re
        django_endblock_re = trans_real.endblock_re

        # Match both Django and Jinja2 translation blocks
        trans_real.block_re = re.compile(
            django_block_re + '|' + jinja_block_re)
        trans_real.endblock_re = re.compile(
            django_endblock_re + '|' + jinja_endblock_re)

        # Call makemessages
        super(Command, self).handle(*args, **options)

        # Restore just the Django-matching regular expressions
        trans_real.endblock_re = django_endblock_re
        trans_real.block_re = django_block_re
