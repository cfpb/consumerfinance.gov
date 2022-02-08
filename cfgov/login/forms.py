import time
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
)
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone

from wagtail.users import forms as wagtailforms

import login.utils
from login.email import send_password_reset_email

from v1.models import base


class PasswordValidationMixin:
    password_key = 'new_password'
    user_attribute = 'user'

    def clean(self):
        cleaned_data = super().clean()
        user = getattr(self, self.user_attribute)
        key1, key2 = (self.password_key + '1', self.password_key + '2')
        if key1 in cleaned_data and key2 in cleaned_data:
            password = cleaned_data[key1]

            login.utils._check_passwords(password,
                                         user,
                                         password_field=key1)
        return cleaned_data


class UserEditValidationMixin(PasswordValidationMixin):
    password_key = 'password'
    user_attribute = 'instance'


class CFGOVPasswordChangeForm(PasswordValidationMixin, PasswordChangeForm):
    pass


class CFGOVPasswordResetForm(PasswordValidationMixin, PasswordResetForm):
    pass


class CFGOVSetPasswordForm(PasswordValidationMixin, SetPasswordForm):
    pass


class LoginForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)

            if (self.user_cache is None and username is not None):
                UserModel = get_user_model()

                try:
                    user = UserModel._default_manager.get(
                        username=username)
                except ObjectDoesNotExist:
                    raise ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username':
                                self.username_field.verbose_name
                                },
                    )

                # fail fast if user is already blocked for some other
                # reason
                self.confirm_login_allowed(user)

                fa, created = base.FailedLoginAttempt.objects.\
                    get_or_create(user=user)
                now = time.time()
                fa.failed(now)
                # Defaults to a 2 hour lockout for a user
                time_period = now - int(settings.LOGIN_FAIL_TIME_PERIOD)
                attempts_allowed = int(settings.LOGIN_FAILS_ALLOWED)
                attempts_used = len(fa.failed_attempts.split(','))

                if fa.too_many_attempts(attempts_allowed, time_period):
                    dt_now = timezone.now()
                    lockout_expires = dt_now + timedelta(
                        seconds=settings.LOGIN_FAIL_TIME_PERIOD)
                    lockout = user.temporarylockout_set.create(
                        expires_at=lockout_expires)
                    lockout.save()
                    raise ValidationError(
                        'This account is temporarily locked; '
                        'please try later or <a href="/admin/password_reset/" '
                        'style="color:white;font-weight:bold">'
                        'reset your password</a>.'
                    )
                else:
                    fa.save()
                    raise ValidationError(
                        'Login failed. {attempts} more attempts until your '
                        'account will be temporarily locked.'.format(
                            attempts=attempts_allowed - attempts_used)
                    )

            else:
                self.confirm_login_allowed(self.user_cache)

                dt_now = timezone.now()
                try:
                    current_password_data = \
                        self.user_cache.passwordhistoryitem_set.latest()

                    if dt_now > current_password_data.expires_at:
                        raise ValidationError(
                            'Your password has expired. Please '
                            '<a href="/admin/password_reset/" '
                            'style="color:white;font-weight:bold">'
                            'reset your password</a>.'
                        )

                except ObjectDoesNotExist:
                    pass

                return self.cleaned_data

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        now = timezone.now()

        lockout_query = user.temporarylockout_set.filter(expires_at__gt=now)

        if lockout_query.count() > 0:
            raise ValidationError(
                'This account is temporarily locked; '
                'please try later or <a href="/admin/password_reset/" '
                'style="color:white;font-weight:bold">'
                'reset your password</a>.'
            )


class UserCreationForm(wagtailforms.UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            User = get_user_model()
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise ValidationError('This email is already in use.')

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            send_password_reset_email(user.email)

        return user


class UserEditForm(wagtailforms.UserEditForm):
    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            User = get_user_model()
            User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise ValidationError('This email is already in use.')
