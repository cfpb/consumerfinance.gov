import re
import secrets

from django.forms import Form
from django.utils.safestring import mark_safe


# Don't allow this to be guessable
_token = secrets.token_hex(20)
_replacements = []


def markup(html: str):
    """
    Exchange some HTML for a unique token that will not be modified by Django's
    HTML escaping.

    On output _replace_tokens() will swap this markup back into place.
    """
    _replacements.append(html)
    return f'{_token}{len(_replacements) - 1}_'


def _replace_labels(html: str) -> str:
    """
    Replace Django's question-level labels with legend elements
    """
    return re.sub(
        '<fieldset><label [^>]+>(.*?)</label>',
        lambda m: f'<fieldset><legend class="tdp-question-legend">{m[1]}</legend>',  # noqa E501
        html,
    )


def _replace_tokens(html: str) -> str:
    """
    Replace the tokens created in markup() with the original markup.

    Because this happens after the HTML escaping in Django, we're able to
    smuggle the original markup unharmed into the output.
    """
    return re.sub(
        f'{_token}(\\d+)_',
        lambda m: _replacements[int(m[1])],
        html,
    )


class SurveyForm(Form):
    """
    Django form subclass to customize markup:

    1. Allow embedding HTML in question titles.
    2. Make Django's markup more accessible for radio button groups.
    """
    def as_ul(self):
        "Return this form rendered as HTML <li>s -- excluding the <ul></ul>."
        output = self._html_output(
            normal_row=''.join([
                '<li%(html_class_attr)s>',
                '<fieldset>%(label)s %(field)s%(help_text)s</fieldset>',
                '</li>'
            ]),
            error_row='<li>%s</li>',
            row_ender='</li>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )
        output = str(output)
        output = _replace_labels(output)
        output = _replace_tokens(output)
        return mark_safe(output)
