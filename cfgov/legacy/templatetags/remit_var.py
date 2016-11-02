import os

from django import template


register = template.Library()


def is_remit():
    if os.environ.get('REMIT', ''):
        return True
    else:
        return False


register.assignment_tag(is_remit)
