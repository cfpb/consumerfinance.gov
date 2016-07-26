from wagtail.wagtailadmin.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.http import HttpRequest


def send_password_reset_email(email):
    form = PasswordResetForm({'email': email})
    if not form.is_valid():
        raise User.DoesNotExist(email)

    template_base = 'wagtailadmin/account/password_reset/'
    form.save(
        HttpRequest(),
        subject_template_name=template_base + 'email_subject.txt',
        email_template_name=template_base + 'email.txt'
    )
