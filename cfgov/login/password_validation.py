import functools
import re
from datetime import timedelta

from django.contrib.auth import hashers
from django.core.exceptions import ValidationError
from django.utils import timezone


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
    """Validate that the password hasn't been changed too recently"""

    def __init__(self, hours):
        self.hours = hours

    def validate(self, password, user=None):
        if user is None:  # pragma: no cover
            return

        # Superusers can always change their password.
        if user.is_superuser:
            return

        # When a new user is created, they should be able to change their
        # initial password right away.
        if user.password_history.count() <= 1:
            return

        latest_password = user.password_history.latest()
        if timezone.now() - latest_password.created <= timedelta(
            hours=self.hours
        ):
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        return (
            f"Password cannot be changed more than once in {self.hours} hours."
        )


class HistoryValidator:
    """Validate that the user doesn't repeat passwords"""

    def __init__(self, count):
        self.count = count

    def validate(self, password, user=None):
        if user is None:  # pragma: no cover
            return

        queryset = user.password_history.order_by("-created")[: self.count]
        checker = functools.partial(hashers.check_password, password)
        if any(
            checker(pass_hist.encrypted_password) for pass_hist in queryset
        ):
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        return f"Password cannot be any of your last {self.count} passwords."
