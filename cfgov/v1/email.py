from django.contrib.auth.models import User
from wagtail.wagtailadmin.forms import PasswordResetForm


def send_password_reset_email(request, email):
    form = PasswordResetForm({'email': email})
    if not form.is_valid():
        raise User.DoesNotExist(email)

    template_base = 'wagtailadmin/account/password_reset/'
    form.save(
        request=request,
        subject_template_name=template_base + 'email_subject.txt',
        email_template_name=template_base + 'email.txt',
        use_https=request.is_secure()
    )
