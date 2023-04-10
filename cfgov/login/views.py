from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


def lockout(request, credentials):
    messages.error(request, "Account is locked.")
    return redirect(reverse_lazy("wagtailadmin_login"))
