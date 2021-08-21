import re
import secrets

from django.forms import Form
from django.utils.safestring import mark_safe


# Don't allow this to be guessable
_token = secrets.token_hex(20)
_replacements = []


def markup(html: str):
    """
    Create a piece of markup that will be rendered in the form as-is with
    no escaping.

    This works by returning an alphanum token that will be replaced with
    the content when the form is rendered.
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
    Replace markup() tokens with the original markup
    """
    return re.sub(
        f'{_token}(\\d+)_',
        lambda m: _replacements[int(m[1])],
        html,
    )


class SurveyForm(Form):
    """
    Form class to customize markup in two ways:
    """
    def as_ul(self):
        "Return this form rendered as HTML <li>s -- excluding the <ul></ul>."
        output = self._html_output(
            normal_row='<li%(html_class_attr)s>%(errors)s<fieldset>%(label)s %(field)s%(help_text)s</fieldset></li>',  # noqa E501
            error_row='<li>%s</li>',
            row_ender='</li>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )
        output = str(output)
        output = _replace_labels(output)
        output = _replace_tokens(output)
        return mark_safe(output)
