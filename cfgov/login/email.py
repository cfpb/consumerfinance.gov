from wagtail.admin.forms.auth import PasswordResetForm


def send_password_reset_email(email):
    form = PasswordResetForm({"email": email})

    if not form.is_valid():
        raise ValueError(email)

    template_base = "wagtailadmin/account/password_reset/"

    form.save(
        domain_override=True,
        subject_template_name=f"{template_base}/email_subject.txt",
        email_template_name=f"{template_base}/email.txt",
    )
