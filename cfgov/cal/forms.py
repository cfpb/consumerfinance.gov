from django import forms

from cal.models import CFPBCalendar
from sheerlike.templates import get_date_string
from v1.util.util import ERROR_MESSAGES


class FilterErrorList(forms.utils.ErrorList):
    def __str__(self):
        return '\n'.join(str(e) for e in self)


class FilterCheckboxList(forms.MultipleChoiceField):
    def validate(self, value):
        if self.required and not value:
            msg = self.error_messages['required']
            if self.label and '%s' in msg:
                msg = msg % self.label
            raise forms.ValidationError(msg, code='required')


class FilterDateField(forms.DateField):
    def clean(self, value):
        if value:
            try:
                value = get_date_string(value)
            except ValueError:
                msg = self.error_messages['invalid']
                if '%s'in msg:
                    msg = msg % value
                raise forms.ValidationError(msg, code='invalid')

        return super(FilterDateField, self).clean(value)


class CalendarFilterForm(forms.Form):
    filter_calendar = FilterCheckboxList(
        required=False,
        label='Calendar',
        error_messages=ERROR_MESSAGES['CHECKBOX_ERRORS']
    )
    filter_range_date_gte = FilterDateField(
        required=False,
        error_messages=ERROR_MESSAGES['DATE_ERRORS']
    )
    filter_range_date_lte = FilterDateField(
        required=False,
        error_messages=ERROR_MESSAGES['DATE_ERRORS']
    )

    def __init__(self, *args, **kwargs):
        super(CalendarFilterForm, self).__init__(*args, **kwargs)
        self.fields['filter_calendar'].choices = [
            (c.title, c.title) for c in CFPBCalendar.objects.all()
        ]

    def clean_filter_calendar(self):
        calendar_names = self.cleaned_data['filter_calendar']
        calendars = CFPBCalendar.objects.filter(title__in=calendar_names)
        return calendars


class CalendarPDFForm(CalendarFilterForm):
    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = FilterErrorList
        super(CalendarPDFForm, self).__init__(*args, **kwargs)
        self.fields['filter_calendar'].required = True

    def clean(self):
        super(CalendarPDFForm, self).clean()
        if (
            not self.cleaned_data.get('filter_range_date_gte') and
            not self.cleaned_data.get('filter_range_date_lte') and
            not self.has_error('filter_range_date_gte') and
            not self.has_error('filter_range_date_lte')
        ):
            raise forms.ValidationError(
                ERROR_MESSAGES['DATE_ERRORS']['one_required']
            )
