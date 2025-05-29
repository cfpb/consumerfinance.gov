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


def get_s3_media_config():
    """Generate S3 file storage configuration from environment.

    Returns tuple of (MEDIA_URL, storage options).
    """
    bucket_name = os.environ["AWS_STORAGE_BUCKET_NAME"]
    location = os.getenv("AWS_S3_STORAGE_LOCATION") or "f"
    custom_domain = os.getenv("AWS_S3_CUSTOM_DOMAIN")

    media_domain = custom_domain or f"{bucket_name}.s3.amazonaws.com"
    media_url = f"https://{media_domain}/{location}/"

    storage_options = {
        # Bucket to use for file storage.
        "bucket_name": bucket_name,
        # Default to bucket ACL.
        "default_acl": None,
        # Do not add auth-related query parameters to S3 URLs.
        # Assumes public access to bucket URLs.
        "querystring_auth": False,
        # Don't overwrite, instead add characters to duplicate filenames.
        # Required by Wagtail, see:
        # https://docs.wagtail.org/en/stable/deployment/under_the_hood.html#cloud-storage.
        "file_overwrite": False,
        # Where in the bucket files get written.
        "location": location,
        # Optionally specify a custom domain for S3 URLs.
        "custom_domain": custom_domain,
    }

    return media_url, storage_options
