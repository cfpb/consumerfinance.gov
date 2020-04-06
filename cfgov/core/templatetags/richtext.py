from django import template


register = template.Library()


@register.filter
def richtext_isempty(value):
    """
    Returns True if a value is None, an empty string, or empty paragraph tags

    Working around known issue https://github.com/wagtail/wagtail/issues/3111.
    Draftail RichTextBlocks passed in require accessing the `source` attribute
    for the comparison.
    """

    blank_values = [None, '', '<p></p>']

    return any([
        value in blank_values,
        hasattr(value, 'source') and value.source in blank_values,
    ])
