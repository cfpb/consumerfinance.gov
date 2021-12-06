from django import forms
from django.test import TestCase

from teachers_digital_platform.forms import SurveyForm, _replace_tokens
from teachers_digital_platform.surveys import (
    ChoiceList, ChoiceQuestion, Survey, SurveyPage, get_survey
)


class SurveyTest(TestCase):

    def test_factory_has_a_whitelist(self):
        survey = get_survey('3-5')
        self.assertIsInstance(survey, Survey)
        survey = get_survey('6-8')
        self.assertIsInstance(survey, Survey)
        survey = get_survey('9-12')
        self.assertIsInstance(survey, Survey)

        with self.assertRaises(AssertionError):
            get_survey('13-14')

    def test_factory(self):
        survey = get_survey('3-5')
        self.assertIsInstance(survey, Survey)
        self.assertEqual(survey.key, '3-5')
        self.assertEqual(survey.meta['name'], 'Grades 3-5')
        self.assertEqual(len(survey.pages), 5)

        page1 = survey.pages[0]
        self.assertIsInstance(page1, SurveyPage)
        self.assertEqual(len(page1.questions), 6)

        q1 = page1.questions[0]
        self.assertIsInstance(q1, ChoiceQuestion)
        self.assertEqual(q1.part, '1')
        self.assertEqual(q1.key, 'q1')
        self.assertEqual(q1.num, 1)
        self.assertEqual(q1.meta, {'atype': 'F'})
        self.assertEqual(q1.answer_values, [5, 4, 3, 2])

        cl = q1.choice_list
        self.assertIsInstance(cl, ChoiceList)
        self.assertEqual(len(cl.choices), 4)
        self.assertEqual(len(cl.labels), 4)
        self.assertEqual(cl.labels[0], 'Most of the time')
        self.assertEqual(cl.choices[0], ('0', 'Most of the time'))

    def test_scoring(self):
        survey = get_survey('3-5')
        page1 = survey.pages[0]
        q1 = page1.questions[0]
        self.assertEqual(q1.get_score('0'), q1.answer_values[0])

    def test_formtools_bugs(self):
        survey = get_survey('3-5')
        page1 = survey.pages[0]
        q1 = page1.questions[0]
        self.assertEqual(q1.get_score(None), q1.answer_values[0])
        self.assertEqual(q1.get_score(''), q1.answer_values[0])

    def test_field_generation(self):
        survey = get_survey('3-5')
        q1 = survey.pages[0].questions[0]
        ret = q1.get_field()
        field = ret['field']
        key = ret['key']

        self.assertEqual(key, 'q1')
        self.assertIsInstance(field, forms.ChoiceField)
        self.assertEqual(field.choices[0], ('0', 'Most of the time'))
        self.assertFalse(field.required)

        # Will be processed by SurveyForm
        expected = _replace_tokens(field.label)
        self.assertEqual(expected, ''.join([
            '<strong class="question-num">1.</strong>',
            ' I make a plan for the things I will do this week.'
        ]))

        self.assertIsInstance(field.widget, forms.RadioSelect)
        self.assertEqual(field.widget.template_name,
                         'teachers_digital_platform/choice.html')
        self.assertEqual(field.widget.attrs['class'], ' '.join([
            'ChoiceField',
            'tdp-survey__choice-question',
            'tdp-survey__atype-F'
        ]))

    def test_page_numbering(self):
        survey = get_survey('3-5')
        self.assertEqual(survey.num_questions_by_page(), [6, 2, 7, 3, 2])

    def test_score_adjusting(self):
        survey = get_survey('3-5')
        self.assertEqual(survey.adjust_total_score(50), 50)
        survey = get_survey('9-12')
        self.assertEqual(survey.adjust_total_score(45), 30)

    def test_form_list(self):
        survey = get_survey('3-5')
        form_list = survey.get_form_list()
        self.assertEqual(len(form_list), 5)

        (page, Form) = form_list[0]
        self.assertEqual(page, 'p1')
        self.assertEqual(Form.__bases__[0], SurveyForm)
        output = Form().as_ul()
        self.assertInHTML(''.join([
            '<legend class="tdp-question-legend">',
            '<strong class="question-num">1.</strong>',
            ' I make a plan for the things I will do this week.',
            '</legend>'
        ]), output)
