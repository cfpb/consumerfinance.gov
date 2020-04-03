from django import template

register = template.Library()


@register.filter
def richtext_isempty(value):
    """
    Returns True if a value is None, an empty string, or empty paragraph tags

    Working around known issue https://github.com/wagtail/wagtail/issues/3111.
    """

    return any([
        value is None,
        value.source == '',
        value.source == '<p></p>',
    ])
