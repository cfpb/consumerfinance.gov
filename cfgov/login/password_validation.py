import re

from django.core.exceptions import ValidationError


class PasswordRegexValidator:
    """Validate that the password matches a given regex"""

    regex = ""
    message = "Enter a valid password"

    def __init__(self, regex=None, message=None):
        if regex is not None:
            self.regex = re.compile(regex)
        if message is not None:
            self.message = message

    def validate(self, password, user=None):
        if not self.regex.search(str(password)):
            raise ValidationError(self.message)

    def get_help_text(self):
        return self.message
