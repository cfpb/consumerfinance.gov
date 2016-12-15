import datetime
from unittest import TestCase

from django import forms

from cal.forms import (CalendarFilterForm, CalendarPDFForm, FilterCheckboxList,
                       FilterDateField)
from cal.models import CFPBCalendar


class FilterCheckboxListTestCase(TestCase):
    def get_field(self, **kwargs):
        return FilterCheckboxList(
            choices=[(c, c) for c in ('a', 'b', 'c')],
            **kwargs
        )

    def test_value_not_required(self):
        self.get_field(required=False).validate('a')

    def test_value_required(self):
        self.get_field().validate('a')

    def test_no_value_not_required(self):
        self.get_field(required=False).validate([])

    def test_no_value_required(self):
        field = self.get_field()
        self.assertRaises(forms.ValidationError, field.validate, None)

    def test_invalid_value_passes(self):
        self.get_field().validate('d')

    def test_multiple_values(self):
        self.get_field().validate(['a', 'b'])

    def test_multiple_values_invalid_passes(self):
        self.get_field().validate(['a', 'd'])

    def test_validation_error_uses_message(self):
        try:
            self.get_field(
                required=True,
                error_messages={'required': 'error message'}
            ).validate(None)
        except forms.ValidationError as e:
            self.assertEqual(e.message, 'error message')
        else:
            self.fail('expected ValidationError')

    def test_validation_error_uses_message_label(self):
        try:
            self.get_field(
                required=True,
                label='widget',
                error_messages={'required': '%s message'}
            ).validate(None)
        except forms.ValidationError as e:
            self.assertEqual(e.message, 'widget message')
        else:
            self.fail('expected ValidationError')


class FilterDateFieldTestCase(TestCase):
    def setUp(self):
        self.field = FilterDateField()

    def test_clean_dashes(self):
        self.assertEqual(
            self.field.clean('2015-01-02'),
            datetime.date(2015, 1, 2)
        )

    def test_clean_slashes(self):
        self.assertEqual(
            self.field.clean('01/02/2015'),
            datetime.date(2015, 1, 2)
        )

    def test_clean_slashes_no_zeros(self):
        self.assertEqual(
            self.field.clean('1/2/15'),
            datetime.date(2015, 1, 2)
        )

    def test_clean_spaces(self):
        self.assertEqual(
            self.field.clean('Jan 2, 2015'),
            datetime.date(2015, 1, 2)
        )

    def test_empty_string_fails_validation(self):
        self.assertRaises(forms.ValidationError, self.field.clean, '')

    def test_none_fails_validation(self):
        self.assertRaises(forms.ValidationError, self.field.clean, None)


class CalendarFormTestCaseMixin(object):
    def setUp(self):
        titles = ['red', 'orange', 'yellow', 'green', 'blue']
        self.calendars = CFPBCalendar.objects.bulk_create([
            CFPBCalendar(pk=i, title=title) for i, title in enumerate(titles)
        ])

    def tearDown(self):
        for calendar in self.calendars:
            calendar.delete()

    def get_form(self, **data):
        return self.form_cls(data=data or {})

    def test_calendar_choices(self):
        form = self.get_form()
        self.assertEqual(
            form.fields['filter_calendar'].choices,
            [(c.title, c.title) for c in self.calendars]
        )

    def test_all_entries_is_valid(self):
        form = self.get_form(
            filter_calendar=['red'],
            filter_range_date_gte='2015-01-02',
            filter_range_date_lte='2016-01-02'
        )
        self.assertTrue(form.is_valid())

    def test_bad_calendar_is_valid(self):
        form = self.get_form(
            filter_calendar=['purple'],
            filter_range_date_gte='2015-01-02',
            filter_range_date_lte='2016-01-02'
        )
        self.assertTrue(form.is_valid())

    def test_cleaned_calendars(self):
        titles = ['red', 'blue']
        form = self.get_form(
            filter_calendar=titles,
            filter_range_date_gte='2015-01-02'
        )
        self.assertTrue(form.is_valid())

        calendars = form.cleaned_data['filter_calendar']
        for title, calendar in zip(titles, calendars):
            self.assertIsInstance(calendar, CFPBCalendar)
            self.assertEqual(calendar.title, title)

    def test_cleaned_bad_calendar(self):
        form = self.get_form(
            filter_calendar=['red', 'purple'],
            filter_range_date_gte='2015-01-02',
            filter_range_date_lte='2016-01-02'
        )
        self.assertTrue(form.is_valid())

        calendars = form.cleaned_data['filter_calendar']
        self.assertEqual(len(calendars), 1)
        self.assertEqual(calendars[0].title, 'red')


class CalendarFilterFormTestCase(CalendarFormTestCaseMixin, TestCase):
    form_cls = CalendarFilterForm

    def test_calendar_choices_not_required(self):
        self.assertFalse(self.get_form().fields['filter_calendar'].required)

    def test_no_entries_is_valid(self):
        self.assertTrue(self.get_form().is_valid())

    def test_only_calendar_is_valid(self):
        form = self.get_form(filter_calendar=['red'])
        self.assertTrue(form.is_valid())

    def test_only_date_is_valid(self):
        form = self.get_form(filter_range_date_gte='2015-01-02')
        self.assertTrue(form.is_valid())


class CalendarPDFFormTestCase(CalendarFormTestCaseMixin, TestCase):
    form_cls = CalendarPDFForm

    def test_calendar_choices_required(self):
        self.assertTrue(self.get_form().fields['filter_calendar'].required)

    def test_no_entries_invalid(self):
        self.assertFalse(self.get_form().is_valid())

    def test_only_calendar_invalid(self):
        form = self.get_form(filter_calendar=['red'])
        self.assertFalse(form.is_valid())

    def test_only_date_invalid(self):
        form = self.get_form(filter_range_date_gte='2015-01-02')
        self.assertFalse(form.is_valid())

    def test_single_date_valid(self):
        form = self.get_form(
            filter_calendar=['red'],
            filter_range_date_gte='2015-01-02'
        )
        self.assertTrue(form.is_valid())

    def test_invalid_date_single_error(self):
        form = self.get_form(
            filter_calendar=['red'],
            filter_range_date_gte='abcde'
        )
        self.assertEqual(len(form.errors), 1)
