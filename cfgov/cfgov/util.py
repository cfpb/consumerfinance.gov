import json
import os

from django.core.exceptions import ImproperlyConfigured


def admin_emails(delimited_list):
    emails = []

    if delimited_list:
        for email in delimited_list.split(";"):
            name_email = email.split("@")
            emails.append((name_email[0], email))

    return emails


def environment_json(variable_name, message=None, default=None):
    """Load an environment variable as JSON to use in settings"""
    try:
        env_value = os.environ.get(variable_name, default)
        json_value = json.loads(env_value)
    except (TypeError, ValueError) as err:
        raise ImproperlyConfigured(message) from err

    return json_value
