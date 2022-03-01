from django import template


register = template.Library()


@register.filter
def richtext_isempty(value):
    """
    Returns True if a value is None, an empty string, or empty paragraph tags

    Working around known issue https://github.com/wagtail/wagtail/issues/3111
    with modification of workaround suggested in
    https://github.com/wagtail/wagtail/issues/4549#issuecomment-500568445.

    Said workaround only worked for RichTextFields. RichTextBlock values
    (wagtail.core.rich_text.RichText) passed in require accessing the `source`
    attribute for the comparison.

    The replace() calls will also ensure that any passed value that amounts to
    nothing but whitespace will also be determined to be empty.
    """

    blank_values = [None, "", "<p></p>"]

    if hasattr(value, "source"):
        # This is a RichTextBlock
        return value.source is None or value.source.replace(" ", "") in blank_values

    # This is a RichTextField
    return value is None or value.replace(" ", "") in blank_values
