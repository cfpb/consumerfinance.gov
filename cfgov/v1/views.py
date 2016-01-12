from core.services import PDFGeneratorView, ICSView
from wagtail.wagtailcore.models import Page
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from wagtail.wagtailadmin import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse


class LeadershipCalendarPDFView(PDFGeneratorView):
    render_url = 'http://localhost/the-bureau/leadership-calendar/print/'
    stylesheet_url = 'http://localhost/static/css/pdfreactor-fonts.css'
    filename = 'cfpb_leadership-calendar.pdf'


class EventICSView(ICSView):
    """
    View for ICS generation in the /events/ section
    """
    # Constants
    event_calendar_prodid = '-//CFPB//Event Calendar//EN',
    event_source = 'http://localhost:9200/content/events/<event_slug>/_source'

    # JSON key names
    event_summary_keyname = 'summary'
    event_dtstart_keyname = 'dtstart'
    event_dtend_keyname = 'dtend'
    event_dtstamp_keyname = 'dtstamp'
    event_uid_keyname = 'uid'
    event_priority_keyname = 'priority'
    event_organizer_keyname = 'organizer'
    event_organizer_addr_keyname = 'organizer_email'
    event_location_keyname = 'location'
    event_status_keyname = 'status'


def renderDirectoryPDF(request):
    pdf = open(settings.V1_TEMPLATE_ROOT + '/the-bureau/about-director/201410_cfpb_bio_cordray.pdf', 'rb').read()

    return HttpResponse(pdf, content_type='application/pdf')


def unshare(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific
    if not page.permissions_for_user(request.user).can_unshare():
        raise PermissionDenied

    if request.method == 'POST':
        page.shared = False
        page.save_revision(user=request.user, submitted_for_moderation=False)
        page.save()

        messages.success(request, _("Page '{0}' unshared.").format(page.title), buttons=[
            messages.button(reverse('wagtailadmin_pages:edit', args=(page.id,)), _('Edit'))
        ])

        return redirect('wagtailadmin_explore', page.get_parent().id)

    return render(request, 'wagtailadmin/pages/confirm_unshare.html', {
        'page': page,
    })


# Override Wagtail Change Password

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash, get_user_model, views as auth_views
from wagtail.wagtailadmin.views import account
from .util import password_policy
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm


def change_password(request):
    if not account.password_management_enabled():
        raise Http404

    can_change_password = request.user.has_usable_password()

    if can_change_password:
        if request.POST:
            form = PasswordChangeForm(user=request.user, data=request.POST)

            if form.is_valid():
                password1 = form.cleaned_data.get('new_password1', '')
                password2 = form.cleaned_data.get('new_password2', '')

                errors = password_policy._check_passwords(password1, password2)

                if len(errors) == 0:
                    form.save()
                    update_session_auth_hash(request, form.user)

                    messages.success(request, _("Your password has been changed successfully!"))
                    return redirect('wagtailadmin_account')
                else:
                    messages.error(request, errors)
                    form = PasswordChangeForm(user=request.user)
        else:
            form = PasswordChangeForm(user=request.user)
    else:
        form = None

    return render(request, 'wagtailadmin/account/change_password.html', {
        'form': form,
        'can_change_password': can_change_password,
    })


from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import resolve_url
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.template.response import TemplateResponse


@sensitive_post_parameters()
@never_cache
def custom_password_reset_confirm(request, uidb64=None, token=None,
                                  template_name='wagtailadmin/account/password_reset/confirm.html',
                                  set_password_form=SetPasswordForm,
                                  post_reset_redirect='wagtailadmin_password_reset_complete'):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    post_reset_redirect = resolve_url(post_reset_redirect)

    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                password1 = form.cleaned_data.get('new_password1', '')
                password2 = form.cleaned_data.get('new_password2', '')
                errors = password_policy._check_passwords(password1, password2)

                if len(errors) == 0:
                    form.save()
                    return HttpResponseRedirect(post_reset_redirect)
                else:
                    messages.error(request, errors)
                    form = set_password_form(user)

        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')

    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }

    return TemplateResponse(request, template_name, context)


password_reset_confirm = account._wrap_password_reset_view(custom_password_reset_confirm)
