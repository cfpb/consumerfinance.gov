import re
from django.conf import settings


def _check_passwords(pass1, pass2):
    """ Run passwords through a set of rules """
    data = ''
    if pass1 != pass2:
        data += "Passwords don't match</br>"
    if pass1 == '':
        data += "Blank passwords are not too secure</br>"
    for rule in settings.CFPB_COMMON_PASSWORD_RULES:
        if not re.search(rule[0], pass1):
            data += (str(rule[1])+"</br>")
    return data
