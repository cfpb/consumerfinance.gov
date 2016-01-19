from django import forms
from django.forms.utils import ErrorList
from django.forms.widgets import DateInput, SelectMultiple
from django.template.loader import get_template
from django.core.context_processors import csrf

from sheerlike.templates import date_formatter
from sheerlike.middleware import get_request
from v1.models.events import EventPage
from jinja2 import FileSystemLoader, exceptions as j2e
from v1 import environment as sheerlike_environment
from util import ERROR_MESSAGES


class FilterField(object):
    def __init__(self, attrs=None, *args, **kwargs):
        self.attrs = attrs
        for base_class in list(self.__class__.__bases__):
            if issubclass(base_class, forms.fields.Field):
                base_class.__init__(self, *args, **kwargs)

    def __str__(self):
        context = dict(value=self.attrs)
        return get_template(self.Media.template).render(context)


class FilterFields:
    #FilterField must be before other Field classes due to MRO
    class CheckboxList(FilterField, forms.fields.MultipleChoiceField):
        error_messages=ERROR_MESSAGES['CHECKBOX_ERRORS']

        def validate(self, value):
            if self.required and not value:
                msg = self.error_messages['required']
                if self.label and '%s' in msg:
                    msg = msg % self.label
                raise forms.ValidationError(msg, code='required')

        class Media:
            template = 'atoms/checkbox-list.html'

    class DateRange(FilterField, forms.fields.MultiValueField):
        error_messages=ERROR_MESSAGES['DATE_ERRORS']

        def validate(self, value):
            if self.required and not value:
                msg = self.error_messages['required']
                if self.label and '%s' in msg:
                    msg = msg % self.label
                raise forms.ValidationError(msg, code='required')

        def to_python(self, value):
            if value:
                try:
                    value = date_formatter(value)
                except Exception as e:
                    pass
            return super(FilterDateField, self).to_python(value)

        class Media:
            template = 'atoms/date-picker.html'


class FilterErrorList(ErrorList):
    def __str__(self):
        return '\n'.join(str(e) for e in self)

class FilterForm(forms.Form):
    attrs = dict(value={})

    def __init__(self, attrs=None, fields=[], *args, **kwargs):
        kwargs['error_class'] = FilterErrorList
        super(FilterForm, self).__init__(*args, **kwargs)
        self.attrs['value'] = attrs
        for field in fields:
            if hasattr(FilterFields, field['type']):
                self.fields[field['type']] = getattr(FilterFields, field['type'])(field)

    def __unicode__(self):
        # This code is copied from
        # https://github.com/django/django/blob/stable/1.8.x/django/forms/forms.py#L206
        # with modifications
        bound_field_errors = []
        for name, field in self.fields.items():
            bound_field = self[name]
            bound_field_errors = self.error_class([conditional_escape(error)
                                 for error in bound_field.errors])
        if len(bound_field_errors):
            self.attrs['value'].update({'errors': bound_field_errors})
        self.attrs['value'].update(dict(csrf(get_request()), fields=self.fields))
        return get_template(self.Media.template).render(self.attrs)

    class Media:
        template = 'organisms/form.html'

class FilterDateField(forms.DateField):
    def to_python(self, value):
        if value:
            try:
                value = date_formatter(value)
            except Exception as e:
                pass
        return super(FilterDateField, self).to_python(value)


class CalenderPDFFilterForm(FilterForm):
    checkbox_list = FilterFields.CheckboxList({
                   'label': 'Calendar',
                   'size' : '1-3',
                   'choices': ['Richard Cordray',
                               'Meredith Fuchs',
                               'Steve Antonakes',
                               'Raj Date',
                               'Elizabeth Warren']})
    date_range = FilterFields.DateRange(dict(legend='Date Range',size='2-3'))

    def clean_filter_calendar(self):
        return self.cleaned_data['filter_calendar'].replace(' ', '+')

    def clean(self):
        cleaned_data = super(CalenderPDFFilterForm, self).clean()
        from_date_empty = 'filter_range_date_gte' in cleaned_data and \
                          cleaned_data['filter_range_date_gte'] == None
        to_date_empty = 'filter_range_date_lte' in cleaned_data and \
                        cleaned_data['filter_range_date_lte'] == None

        if from_date_empty and to_date_empty :
            raise forms.ValidationError(ERROR_MESSAGES['DATE_ERRORS']['one_required'])
        return cleaned_data


class EventsFilterForm(forms.Form):
    tags_select_attrs = {
        'class': 'chosen-select',
        'multiple': 'multiple',
        'data-placeholder': 'Search for topics',
    }
    from_select_attrs = {
        'class': 'js-filter_range-date js-filter_range-date__gte',
        'type': 'text',
        'placeholder': 'YYYY-MM',
    }
    to_select_attrs = from_select_attrs.copy()
    to_select_attrs.update({
        'class': 'js-filter_range-date js-filter_range-date__lte',
    })

    from_date = forms.DateField(required=False, input_formats=['%Y-%m-%d'],
                                widget=DateInput(attrs=from_select_attrs))
    to_date = forms.DateField(required=False, input_formats=['%Y-%m-%d'],
                              widget=DateInput(attrs=to_select_attrs))
    topics = forms.MultipleChoiceField(required=False, choices=[],
                                       widget=SelectMultiple(attrs=tags_select_attrs))
    @property
    def field_queries(self):
        return zip(['start_dt__gte', 'end_dt__lte', 'tags__name__in'],
                   ['from_date', 'to_date', 'topics'])

    def __init__(self, *args, **kwargs):
        super(EventsFilterForm, self).__init__(*args, **kwargs)

        if 'topics' in self.fields:
            options = list(set([tag for tags in [event.tags.names() for event
                                                 in EventPage.objects.live()]
                                for tag in tags]))
            most = [(option, option) for option in options[:3]]
            other = [(option, option) for option in options[3:]]

            self.fields['topics'].choices = (('Most frequent', tuple(most)),
                                             ('All other topics', tuple(other)))
