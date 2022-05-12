from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest

from wagtail.admin.forms.auth import PasswordResetForm
from wagtail.core.models import Site


def create_request_for_email(method="GET"):
    """
    Create an HttpRequest object suitable for use in Django email
    forms with appropriate hostname and ports. Requires a configured
    default Wagtail Site object.
    """
    try:
        site = Site.objects.get(is_default_site=True)
    except Site.DoesNotExist:
        raise RuntimeError("no default wagtail site configured")

    return WSGIRequest(
        {
            "REQUEST_METHOD": method,
            "SERVER_NAME": site.hostname,
            "SERVER_PORT": site.port,
            "wsgi.input": "",
            "wsgi.url_scheme": "https" if 443 == site.port else "http",
        }
    )


def send_password_reset_email(email, request=None):
    form = PasswordResetForm({"email": email})
    if not form.is_valid():
        raise User.DoesNotExist(email)

    request = request or create_request_for_email()

    template_base = "wagtailadmin/account/password_reset/"
    form.save(
        request=request,
        subject_template_name=template_base + "email_subject.txt",
        email_template_name=template_base + "email.txt",
        use_https=request.is_secure(),
    )
