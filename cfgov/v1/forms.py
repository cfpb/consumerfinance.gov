import time
from datetime import timedelta

from django import forms
from django.forms.utils import ErrorList
from django.forms.widgets import DateInput, SelectMultiple
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

from sheerlike.query import QueryFinder
from sheerlike.templates import date_formatter
from v1.models.events import EventPage
from util import ERROR_MESSAGES

# importing wagtail.wagtailadmin.forms at module load time seems to have
# caused some trouble with the translation subsystem being invoked before
# it's ready-- so I've wrapped it in a function
def login_form():
    from wagtail.wagtailadmin import forms as wagtail_adminforms
    from v1.util import password_policy

    from .models import base
    class LoginForm(wagtail_adminforms.LoginForm):

        def clean(self):
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')

            if username and password:
                self.user_cache = authenticate(username=username,
                  password=password)

                if (self.user_cache is None and username is not None):
                    UserModel = get_user_model()

                    try: 
                        user = UserModel._default_manager.get(username=username)
                    except ObjectDoesNotExist:
                        raise forms.ValidationError(
                            self.error_messages['invalid_login'],
                            code='invalid_login',
                            params={'username': self.username_field.verbose_name},
                        )

                    # fail fast if user is already blocked for some other reason
                    self.confirm_login_allowed(user) 

                    fa, created = base.FailedLoginAttempt.objects.get_or_create(user=user)
                    now = time.time()
                    fa.failed(now)
                    # Defaults to a 2 hour lockout for a user
                    time_period = now - int(settings.LOGIN_FAIL_TIME_PERIOD)
                    attempts_allowed = int(settings.LOGIN_FAILS_ALLOWED)
                    attempts_used = len(fa.failed_attempts.split(','))

                    if fa.too_many_attempts(attempts_allowed, time_period):
                        dt_now = timezone.now()
                        lockout_expires = dt_now + timedelta(seconds=settings.LOGIN_FAIL_TIME_PERIOD)
                        lockout = user.temporarylockout_set.create(expires_at=lockout_expires)
                        lockout.save()
                        raise ValidationError("This account is temporarily locked; please try later or reset your password")
                    else:
                        fa.save()
                        raise ValidationError('Login failed. %s more attempts until your account will be temporarily locked.' % (attempts_allowed-attempts_used))

                else:
                    self.confirm_login_allowed(self.user_cache)

                    dt_now = timezone.now()
                    try:
                        current_password_data = self.user_cache.passwordhistoryitem_set.latest()
                    
                        if dt_now > current_password_data.expires_at:
                            raise ValidationError("This password has expired; please reset your password")

                    except ObjectDoesNotExist:
                        pass

                    return self.cleaned_data

        def confirm_login_allowed(self, user):
            super(LoginForm, self).confirm_login_allowed(user)
            now = timezone.now()

            lockout_query = user.temporarylockout_set.filter(expires_at__gt=now)

            if lockout_query.count() > 0 :
                raise ValidationError("This account is temporarily locked; please try later or reset your password")


    return LoginForm

class FilterErrorList(ErrorList):
    def __str__(self):
        return '\n'.join(str(e) for e in self)

class FilterDateField(forms.DateField):
    def to_python(self, value):
        if value:
            try:
                value = date_formatter(value)
            except Exception as e:
                pass
        return super(FilterDateField, self).to_python(value)

class FilterCheckboxList(forms.CharField):
    def validate(self, value):
        if value in self.empty_values and self.required:
            msg = self.error_messages['required']
            if self.label and '%s' in msg:
                msg = msg % self.label
            raise forms.ValidationError(msg, code='required')

class CalenderPDFFilterForm(forms.Form):
    filter_calendar = FilterCheckboxList(label='Calendar',
        error_messages=ERROR_MESSAGES['CHECKBOX_ERRORS'])
    filter_range_date_gte = FilterDateField(required=False,
        error_messages=ERROR_MESSAGES['DATE_ERRORS'])
    filter_range_date_lte = FilterDateField(required=False,
        error_messages=ERROR_MESSAGES['DATE_ERRORS'])

    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = FilterErrorList
        super(CalenderPDFFilterForm, self).__init__(*args, **kwargs)

    def clean_filter_calendar(self):
        return self.cleaned_data['filter_calendar'].replace(' ', '+')

    def clean(self):
        cleaned_data = super(CalenderPDFFilterForm, self).clean()
        from_date_empty = 'filter_range_date_gte' in cleaned_data and \
                          cleaned_data['filter_range_date_gte']  == None
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
