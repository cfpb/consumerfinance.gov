import re
import secrets

from django.forms import Form
from django.utils.safestring import SafeData, mark_safe


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


def _replace_tokens(html: str) -> SafeData:
    html = re.sub(
        f'{_token}(\\d+)_',
        lambda m: _replacements[int(m[1])],
        html,
    )

    return mark_safe(html)


class AssessmentForm(Form):
    def as_p(self):
        "Return this form rendered as HTML <p>s."
        output = self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',  # noqa: E501
            error_row='%s',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True,
        )
        return _replace_tokens(str(output))
