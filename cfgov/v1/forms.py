from django import forms
from django.forms.widgets import DateInput, SelectMultiple
from v1.models.events import EventPage
from sheerlike.templates import date_formatter


class CalenderPDFFilterForm(forms.Form):
    filter_calendar = forms.CharField()
    filter_range_date_gte = forms.DateField(input_formats=['%Y-%m-%d'])
    filter_range_date_lte = forms.DateField(input_formats=['%Y-%m-%d'])

    def __init__(self, *args, **kwargs):
        if(args[0]):
            formDict = args[0].copy()
            date_gte = formDict.get('filter_range_date_gte')
            date_lte = formDict.get('filter_range_date_lte')
            if(date_gte):
                formDict.__setitem__('filter_range_date_gte', date_formatter(date_gte))
            if(date_lte):
                formDict.__setitem__('filter_range_date_lte', date_formatter(date_lte))
            args = list(args)
            args[0] = formDict

        super(CalenderPDFFilterForm, self).__init__(*args, **kwargs)

    def clean_filter_calendar(self):
        return self.cleaned_data['filter_calendar'].replace(' ', '+')


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
