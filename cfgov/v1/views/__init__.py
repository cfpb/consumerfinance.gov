import django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.template.response import TemplateResponse
from django.urls import resolve
from django.utils.encoding import force_str
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from wagtail.admin.views import account

from v1.auth_forms import (
    CFGOVPasswordChangeForm, CFGOVSetPasswordForm, LoginForm
)
from v1.util.util import all_valid_destinations_for_request
from v1.util.wrap_password_reset import _wrap_password_reset_view


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

            messages.success(
                request,
                _("Your password has been changed successfully!")
            )
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
@csrf_protect
@never_cache
def login_with_lockout(request, template_name='wagtailadmin/login.html'):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME,
                                                   '/admin/'))
    # Redirects to https://example.com should not be allowed.
    if redirect_to:
        if '//' in redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if django.VERSION > (2, 0):
                if not is_safe_url(
                    url=redirect_to, allowed_hosts=request.get_host()
                ):
                    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            else:
                if not is_safe_url(url=redirect_to, host=request.get_host()):
                    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            user = form.get_user()
            try:
                user.failedloginattempt.delete()
            except ObjectDoesNotExist:
                pass

            login(request, form.get_user())

            return HttpResponseRedirect(
                '/login/check_permissions/?next=' + redirect_to)
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(
                '/login/check_permissions/?next=' + redirect_to)
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


@never_cache
def check_permissions(request):
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''))

    if not is_safe_url(url=redirect_to, allowed_hosts=request.get_host()):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    if not request.user.is_authenticated:
        return HttpResponseRedirect(
            "%s?%s=%s" % (settings.LOGIN_URL, REDIRECT_FIELD_NAME, redirect_to)
        )

    view, args, kwargs = resolve(redirect_to)
    kwargs['request'] = request
    try:
        response = view(*args, **kwargs)
    except (Http404, TypeError):
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    if isinstance(response, HttpResponseRedirect):
        # this indicates a permissions problem
        # (there may be a better way)
        if REDIRECT_FIELD_NAME + '=' in response.url:
            return render(
                request,
                "wagtailadmin/access_denied.html",
                context={
                    'attempted_to_reach': redirect_to,
                    'destinations': all_valid_destinations_for_request(request)
                }
            )

    return HttpResponseRedirect(redirect_to)


@sensitive_post_parameters()
@never_cache
def custom_password_reset_confirm(
        request, uidb64=None, token=None,
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
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = CFGOVSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
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


password_reset_confirm = _wrap_password_reset_view(
    custom_password_reset_confirm)
