from django import forms
from django.core import signing
from django.test import TestCase

from teachers_digital_platform.forms import SharedUrlForm, SurveyForm, markup
from teachers_digital_platform.UrlEncoder import UrlEncoder


_key = '3-5'
_scores = [0, 10, 15]
_time = 1623518461
_code = UrlEncoder([_key]).dumps(_key, _scores, _time)
_signed_code = signing.Signer().sign(_code)


class SharedFormTest(TestCase):

    def test_valid_signed_code(self):
        form = SharedUrlForm({'r': _signed_code})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['r'], (_signed_code, _code))

    def test_rejects_modification(self):
        _modified = _signed_code[0:5] + 'z' + _signed_code[5]
        form = SharedUrlForm({'r': _modified})
        self.assertFalse(form.is_valid())

    def test_rejects_missing(self):
        form = SharedUrlForm({})
        self.assertFalse(form.is_valid())


class SurveyFormTest(TestCase):

    def test_as_ul_uses_fieldsets(self):
        class TestForm(SurveyForm):
            q1 = forms.CharField(
                label='Hello.',
                required=False,
            )

        form = TestForm()
        output: str = form.as_ul()
        expected = ''.join([
            '<li><fieldset>',
            '<legend class="tdp-question-legend">Hello.</legend>'
        ])
        actual = output[0:len(expected)]

        self.assertEqual(actual, expected)

    def test_markup_in_question_title(self):
        class TestForm(SurveyForm):
            q1 = forms.CharField(label=markup('<b>One</b> <i>Two</i>'))

        form = TestForm()
        output: str = form.as_ul()

        self.assertInHTML('<b>One</b>', output)
        self.assertInHTML('<i>Two</i>', output)
