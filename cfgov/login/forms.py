from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone

from wagtail.admin.forms.auth import AuthenticationForm
from wagtail.users import forms as wagtailforms

from login.email import send_password_reset_email


class PasswordExpiredError(ValidationError):
    """A validation error due to password expiration"""

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
