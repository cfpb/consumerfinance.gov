from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect, render

from wagtail.admin.views import account
from wagtail.admin.views.account import LoginView as WagtailLoginView
from wagtail.admin.views.account import PasswordResetConfirmView

from login.forms import CFGOVPasswordChangeForm, CFGOVSetPasswordForm


# Override the Wagtail PasswordResetConfirmView to use our custom password
# set form and remove lockouts when the form is valid.
class CFGOVPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CFGOVSetPasswordForm

    def form_valid(self, form):
        self.user.temporarylockout_set.all().delete()
        return super().form_valid(form)


# Overrided Django Views
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
                request, "Your password has been changed successfully!"
            )
            return redirect("wagtailadmin_account")
        else:
            if "__all__" in form.errors:
                for error in form.errors["__all__"]:
                    messages.error(request, error)
    else:
        form = CFGOVPasswordChangeForm(user=request.user)

    return render(
        request,
        "wagtailadmin/account/change_password.html",
        {
            "form": form,
            "can_change_password": can_change_password,
        },
    )


class LoginView(WagtailLoginView):
    def form_valid(self, form):
        response = super().form_valid(form)

        # After successful login, remove any failed login attempts.
        user = form.get_user()
        try:
            user.failedloginattempt.delete()
        except ObjectDoesNotExist:
            pass

        return response
