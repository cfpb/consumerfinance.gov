import functools
import re

from django.conf import settings
from django.contrib.auth import hashers
from django.core.exceptions import ObjectDoesNotExist, ValidationError


def validate_password_rule(
    regex, password, password_field, failure_message="invalid password"
):
    if not re.search(regex, password):
        raise ValidationError({password_field: failure_message})


def validate_password_all_rules(password, password_field):
    for regex, rule_name in settings.CFPB_COMMON_PASSWORD_RULES:
        validate_password_rule(regex, password, password_field, rule_name)


def validate_password_age(user):
    try:
        current_password_data = user.passwordhistoryitem_set.latest()

        if not current_password_data.can_change_password():
            raise ValidationError(
                "You can not change passwords more than once in 24 hours"
            )
    except ObjectDoesNotExist:
        pass


def validate_password_history(user, password):
    queryset = user.passwordhistoryitem_set.order_by("-created")[:10]

    checker = functools.partial(hashers.check_password, password)

    if any(checker(pass_hist.encrypted_password) for pass_hist in queryset):
        raise ValidationError("You may not re-use any of your last 10 passwords")


def _check_passwords(password, user, password_field):
    if user:
        validate_password_age(user)
        validate_password_history(user, password)
    validate_password_all_rules(password, password_field)
