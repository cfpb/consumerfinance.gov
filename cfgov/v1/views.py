from core.services import PDFGeneratorView, ICSView
from wagtail.wagtailcore.models import Page
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from wagtail.wagtailadmin import messages as wagtail_messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash,\
        REDIRECT_FIELD_NAME, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.template.response import TemplateResponse

from wagtail.wagtailadmin.views import account
from wagtail.wagtailusers.views.users import add_user_perm, change_user_perm
from wagtail.wagtailadmin.utils import permission_required

from .auth_forms import CFGOVUserCreationForm, CFGOVUserEditForm,\
    CFGOVSetPasswordForm, CFGOVPasswordChangeForm, LoginForm

from .signals import page_unshared


class LeadershipCalendarPDFView(PDFGeneratorView):
    render_url = 'http://localhost/about-us/the-bureau/leadership-calendar/print/'
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

        page_unshared.send(sender=page.specific_class, instance=page.specific)

        wagtail_messages.success(request, _("Page '{0}' unshared.").format(page.title), buttons=[
            wagtail_messages.button(reverse('wagtailadmin_pages:edit', args=(page.id,)), _('Edit'))
        ])

        return redirect('wagtailadmin_explore', page.get_parent().id)

    return render(request, 'wagtailadmin/pages/confirm_unshare.html', {
        'page': page,
    })


# Overrided Wagtail Views
@login_required
def change_password(request):
    if not account.password_management_enabled():
        raise Http404

    user = request.user
    can_change_password = user.has_usable_password()

    if not can_change_password:
        form = None

    if request.POST:
        form = CFGOVPasswordChangeForm(user=user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            messages.success(request, _("Your password has been changed successfully!"))
            return redirect('wagtailadmin_account')
        else:
            if '__all__' in form.errors:
                for error in form.errors['__all__']:
                    messages.error(request, error)
    else:
        form = CFGOVPasswordChangeForm(user=request.user)

    return render(request, 'wagtailadmin/account/change_password.html', {
        'form': form,
        'can_change_password': can_change_password,
    })


@sensitive_post_parameters()
@never_cache
def cfpb_login(request):
    if request.user.is_authenticated():
        if request.user.has_perm('wagtailadmin.access_admin'):
            return redirect('wagtailadmin_home')
        else:
            return render(request, "wagtailadmin/access_denied.html")

    else:
        return login_with_lockout(request)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_with_lockout(request, template_name='wagtailadmin/login.html'):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''))

    # redirects to http://example.com should not be allowed
    if redirect_to:
        if '//' in redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            user = form.get_user()
            try:
                user.failedloginattempt.delete()
            except ObjectDoesNotExist:
                pass

            login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = LoginForm(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        REDIRECT_FIELD_NAME: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }

    context.update({'show_password_reset': account.password_reset_enabled(),
                    'username_field': get_user_model().USERNAME_FIELD, })

    return TemplateResponse(request, template_name, context)



@sensitive_post_parameters()
@never_cache
def custom_password_reset_confirm(request, uidb64=None, token=None,
                                  template_name='wagtailadmin/account/password_reset/confirm.html',
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
            form = CFGOVSetPasswordForm(user, request.POST)
            if form.is_valid():
                    user.temporarylockout_set.all().delete()
                    return HttpResponseRedirect(post_reset_redirect)

        else:
            form = CFGOVSetPasswordForm(user)
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

## User Creation




@permission_required(add_user_perm)
def create_user(request):
    if request.POST:
        form = CFGOVUserCreationForm(request.POST)
        if form.is_valid():
                user = form.save()
                wagtail_messages.success(request, _("User '{0}' created.").format(user), buttons=[
                    wagtail_messages.button(reverse('wagtailusers_users:edit', args=(user.id,)), _('Edit'))
                ])
                return redirect('wagtailusers_users:index')
        elif '__all__' in form.errors:
                wagtail_messages.error(request,form.errors['__all__'])
    else:
        form = CFGOVUserCreationForm()

    return render(request, 'wagtailusers/users/create.html', {
        'form': form,
    })

@permission_required(change_user_perm)
def edit_user(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.POST:
        form = CFGOVUserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            user.temporarylockout_set.all().delete()
            wagtail_messages.success(request, _("User '{0}' updated.").format(user), buttons=[
                wagtail_messages.button(reverse('wagtailusers_users:edit', args=(user.id,)), _('Edit'))
            ])
            return redirect('wagtailusers_users:index')
        else:
            if '__all__' in form.errors:
                wagtail_messages.error(request,form.errors['__all__'])
    else:
        form = CFGOVUserEditForm(instance=user)

    return render(request, 'wagtailusers/users/edit.html', {
        'user': user,
        'form': form,
    })
