from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone

from wagtail.admin.forms.auth import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
)
from wagtail.users import forms as wagtailforms

import login.utils
from login.email import send_password_reset_email


class PasswordExpiredError(ValidationError):
    """A validation error due to password expiration"""

    pass


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
        "password_expired": (
            "Your password has expired. Please "
            '<a href="/admin/password_reset/" style="color:white;font-weight:bold">'
            "reset your password</a>."
        ),
        **AuthenticationForm.error_messages,
    }

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        # Check to make sure the user's password hasn't expired.
        self.check_for_password_expiration(user)

    def check_for_password_expiration(self, user):
        dt_now = timezone.now()
        try:
            current_password_data = user.passwordhistoryitem_set.latest()

            if dt_now > current_password_data.expires_at:
                raise PasswordExpiredError(
                    self.error_messages["password_expired"],
                    code="password_expired",
                )
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
