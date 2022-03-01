import unicodedata

from django import template


register = template.Library()


def strip_accents(value):
    nfkd_form = unicodedata.normalize("NFKD", value)
    only_ascii = nfkd_form.encode("ASCII", "ignore")
    return only_ascii


register.filter("stripaccents", strip_accents)
