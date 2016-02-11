import functools
import re

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import hashers
from django.core.exceptions import ObjectDoesNotExist


def _check_passwords(pass1, pass2, user):
    """ Run passwords through a set of rules """
    data = ''
    if pass1 != pass2:
        data += "Passwords don't match</br>"
    if pass1 == '':
        data += "Blank passwords are not too secure</br>"
    for rule in settings.CFPB_COMMON_PASSWORD_RULES:
        if not re.search(rule[0], pass1):
            data += (str(rule[1])+"</br>")


    if len(data)==0: # only check this stuff if there are no failures above
        from ..models import PasswordHistoryItem
        try:
            current_password_data = user.passwordhistoryitem_set.latest()

            if not current_password_data.can_change_password():
                data += "You can not change passwords more than once" \
                              " in 24 hours"
        except ObjectDoesNotExist:
            pass

    if len(data)==0:
        queryset = user.passwordhistoryitem_set.order_by('-created')[:10]

        checker =functools.partial(hashers.check_password, pass1)

        if any([checker(pass_hist.encrypted_password) for pass_hist in queryset]):
            data += "You may not re-use any of your last 10 passwords"

    return data
