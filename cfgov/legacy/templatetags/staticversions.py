from django import template
from django.conf import settings


register = template.Library()


def get_static_version():
    return '%s%s' % ('?ver=', settings.STATIC_VERSION)


register.simple_tag(get_static_version)
