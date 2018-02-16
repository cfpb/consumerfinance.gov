import unicodedata
from six import text_type as unicode

from django import template


register = template.Library()


def strip_accents(value):
    nfkd_form = unicodedata.normalize('NFKD', unicode(value))
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

register.filter('stripaccents', strip_accents)
