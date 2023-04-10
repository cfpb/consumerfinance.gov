import functools
import re

from django.contrib.auth import hashers
from django.core.exceptions import ValidationError

from login.models import PasswordHistoryItem


class ComplexityValidator:
    """Validate that the password meets a set of complexity rules"""

    def __init__(self, rules=None):
        self.rules = rules or []

    def validate(self, password, user=None):
        for rule_re, message in self.rules:
            if not re.search(rule_re, password):
                raise ValidationError(
                    message,
                    code="password_complexity",
                )

    def get_help_text(self):
        return "; ".join([m for r, m in self.rules])


class AgeValidator:
    """Validate that the password is more than 24 hours old"""

    def validate(self, password, user=None):
        if user is None:  # pragma: no cover
            return

        try:
            current_password_data = user.passwordhistoryitem_set.latest()
            if not current_password_data.can_change_password():
                raise ValidationError(self.get_help_text())
        except PasswordHistoryItem.DoesNotExist:
            pass

    def get_help_text(self):
        return "Password cannot be changed more than once in 24 hours."


class HistoryValidator:
    """Validate that the password hasn't been one of the user's last 10"""

    def validate(self, password, user=None):
        queryset = user.passwordhistoryitem_set.order_by("-created")[:10]
        checker = functools.partial(hashers.check_password, password)
        if any(
            checker(pass_hist.encrypted_password) for pass_hist in queryset
        ):
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        return "Password cannot be any of your last 10 passwords."
