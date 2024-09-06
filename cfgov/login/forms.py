from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from wagtail.users import forms as wagtailforms


User = get_user_model()


class UserCreationForm(wagtailforms.UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already in use.")

        return email


class UserEditForm(wagtailforms.UserEditForm):
    def clean_email(self):
        email = self.cleaned_data["email"]

        if (
            User.objects.exclude(pk=self.instance.pk)
            .filter(email__iexact=email)
            .exists()
        ):
            raise ValidationError("This email is already in use.")

        return email
