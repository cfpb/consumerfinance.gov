from django import forms
from django.test import TestCase

from ..forms import SurveyForm, markup


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
