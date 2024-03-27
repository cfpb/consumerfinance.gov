from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from django.utils.safestring import mark_safe

from wagtail.admin.forms.auth import LoginForm as WagtailLoginForm
from wagtail.users import forms as wagtailforms

from login.email import send_password_reset_email


class LoginForm(WagtailLoginForm):
    PASSWORDS_EXPIRE_IN_DAYS = 90

    error_messages = {
        "password_expired": (
            mark_safe(
                "Your password has expired. Please "
                '<a href="/admin/password_reset/" style="color:white;font-weight:bold">'
                "reset your password</a>."
            )
        ),
        **WagtailLoginForm.error_messages,
    }

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        # Check to make sure the user's password hasn't expired.
        self.check_for_password_expiration(user)

    def check_for_password_expiration(self, user):
        try:
            latest_password = user.password_history.latest()
        except ObjectDoesNotExist:
            return

        if timezone.now() - latest_password.created >= timedelta(
            days=self.PASSWORDS_EXPIRE_IN_DAYS
        ):
            raise ValidationError(
                self.error_messages["password_expired"],
                code="password_expired",
            )


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
