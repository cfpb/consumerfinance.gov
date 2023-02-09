import time
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone

from wagtail.users import forms as wagtailforms

import login.utils
from login.email import send_password_reset_email
from login.models import FailedLoginAttempt


class PasswordValidationMixin:
    password_key = "new_password"  # nosec
    user_attribute = "user"

    def clean(self):
        cleaned_data = super().clean()
        user = getattr(self, self.user_attribute)
        key1, key2 = (self.password_key + "1", self.password_key + "2")
        if key1 in cleaned_data and key2 in cleaned_data:
            password = cleaned_data[key1]

            login.utils._check_passwords(password, user, password_field=key1)
        return cleaned_data


class UserEditValidationMixin(PasswordValidationMixin):
    password_key = "password"  # nosec
    user_attribute = "instance"


class CFGOVPasswordChangeForm(PasswordValidationMixin, PasswordChangeForm):
    pass


class CFGOVPasswordResetForm(PasswordValidationMixin, PasswordResetForm):
    pass


class CFGOVSetPasswordForm(PasswordValidationMixin, SetPasswordForm):
    pass


class LoginForm(AuthenticationForm):
    error_messages = {
        "temporary_lock": (
            "This account is temporarily locked; please try later or "
            '<a href="/admin/password_reset/" style="color:white;font-weight:bold">'
            "reset your password</a>."
        ),
        "password_expired": (
            "Your password has expired. Please "
            '<a href="/admin/password_reset/" style="color:white;font-weight:bold">'
            "reset your password</a>."
        ),
        **AuthenticationForm.error_messages,
    }

    def clean(self):
        try:
            return super().clean()
        except ValidationError as e:
            # The Django AuthenticationForm raised a validation error because
            # it could not authenticate the username/password combination.
            #
            # We want to record the failed login attempt, and maybe raise a
            # lockout validation error of our own before raising Django's
            self.record_failed_login_attempt(self.cleaned_data["username"])
            raise e

    def record_failed_login_attempt(self, username):
        UserModel = get_user_model()

        try:
            user = UserModel._default_manager.get(username=username)
        except ObjectDoesNotExist:
            raise self.get_invalid_login_error()

        fa, created = FailedLoginAttempt.objects.get_or_create(user=user)
        now = time.time()
        fa.failed(now)

        # Defaults to a 2 hour lockout for a user
        time_period = now - settings.LOGIN_FAIL_TIME_PERIOD
        attempts_allowed = settings.LOGIN_FAILS_ALLOWED

        if fa.too_many_attempts(attempts_allowed, time_period):
            dt_now = timezone.now()
            lockout_expires = dt_now + timedelta(
                seconds=settings.LOGIN_FAIL_TIME_PERIOD
            )
            lockout = user.temporarylockout_set.create(
                expires_at=lockout_expires
            )
            lockout.save()
            raise ValidationError(
                self.error_messages["temporary_lock"],
                code="temporary_lock",
            )
        else:
            fa.save()

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        # Check to make sure the user is not already locked out.
        self.check_for_lockout(user)

        # Check to make sure the user's password hasn't expired.
        self.check_for_password_expiration(user)

        # Finally, clear any failed login attempts
        self.clear_failed_login_attempts(user)

    def check_for_lockout(self, user):
        now = timezone.now()
        lockout_query = user.temporarylockout_set.filter(expires_at__gt=now)
        if lockout_query.count() > 0:
            raise ValidationError(
                self.error_messages["temporary_lock"],
                code="temporary_lock",
            )

    def check_for_password_expiration(self, user):
        dt_now = timezone.now()
        try:
            current_password_data = user.passwordhistoryitem_set.latest()

            if dt_now > current_password_data.expires_at:
                raise ValidationError(
                    self.error_messages["password_expired"],
                    code="password_expired",
                )
        except ObjectDoesNotExist:
            pass

    def clear_failed_login_attempts(self, user):
        try:
            user.failedloginattempt.delete()
        except ObjectDoesNotExist:
            pass


class UserCreationForm(wagtailforms.UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User = get_user_model()
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise ValidationError("This email is already in use.")

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            send_password_reset_email(user.email)

        return user


class UserEditForm(wagtailforms.UserEditForm):
    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User = get_user_model()
            User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise ValidationError("This email is already in use.")
