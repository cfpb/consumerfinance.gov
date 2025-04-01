import os
import sys
from os.path import exists

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.utils.text import format_lazy

from cfgov.settings.base import *
from cfgov.util import environment_json


default_loggers = []

# Is there a syslog device available?
# selects first of these locations that exist, or None
syslog_device = next(
    (l for l in ["/dev/log", "/var/run/syslog"] if exists(l)), None
)

if syslog_device:
    default_loggers.append("syslog")

# if not running in mod_wsgi, add console logger
if not (sys.argv and sys.argv[0] == "mod_wsgi"):
    default_loggers.append("console")

# Sends an email to developers in the ADMIN_EMAILS list if Debug=False for errors
#
# in the formatter, "django: " is an rsyslog tag. This is equivalent to:
#     logger -t django "my log message"
# on the server, the tag will be used to route the message to the desired
# logfile
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "tagged": {"format": "django: %(message)s"},
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": [],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
        "django": {
            "level": "ERROR",
            "propagate": False,
        },
        "": {
            "handlers": default_loggers,
            "level": "INFO",
            "propagate": True,
        },
    },
}

if os.environ.get("SQS_QUEUE_ENABLED"):
    LOGGING["handlers"]["sqs"] = {
        "level": "ERROR",
        "class": "alerts.logging_handlers.CFGovErrorHandler",
    }
    LOGGING["loggers"]["django.request"]["handlers"].append("sqs")

# Only add syslog to LOGGING if it's in default_loggers
if "syslog" in default_loggers:
    LOGGING["handlers"]["syslog"] = {
        "address": syslog_device,
        "class": "logging.handlers.SysLogHandler",
        "formatter": "tagged",
    }

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
DEFAULT_FROM_EMAIL = "wagtail@cfpb.gov"

STORAGES["staticfiles"] = {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}

# ALLOWED_HOSTS should be defined as a JSON list in the ALLOWED_HOSTS
# environment variable.
ALLOWED_HOSTS = environment_json(
    "ALLOWED_HOSTS",
    (
        "Environment variable ALLOWED_HOSTS is either not defined or is "
        "not valid JSON. Expected a JSON array of allowed hostnames."
    ),
)

# Django baseline required settings
SECURE_REFERRER_POLICY = "same-origin"
SESSION_COOKIE_SAMESITE = "Strict"
X_FRAME_OPTIONS = "SAMEORIGIN"
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_PRELOAD = True

# In production deployments SSL is never terminated at the Django application,
# so in practice Django will never receive secure requests. HTTP requests must
# always come with an "X-Forwarded-Proto: https" header if this is set to True
# or this we get into a redirect loop.
SECURE_SSL_REDIRECT = False

# Require the SECRET_KEY as an environment variable
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ImproperlyConfigured(
        "The SECRET_KEY environment variable must be set"
    )

# Secret key fallbacks that allow the rotation of the secret key.
# This environment variable should be a JSON array if fallbacks are available.
# This list is empty (no old fallback secret keys) if the environment variable
# SECRET_KEY_FALLBACKS is not set.
SECRET_KEY_FALLBACKS = environment_json(
    "SECRET_KEY_FALLBACKS",
    (
        "Environment variable SECRET_KEY_FALLBACKS is not valid JSON. "
        "Expected a JSON array of fallback secret keys."
    ),
    default="[]",
)

if ENABLE_SSO:
    # We need the OIDC identity provider to be able to send the sessionid to
    # the OIDC callback view in order to validate the OIDC state
    SESSION_COOKIE_SAMESITE = "Lax"

    LOGGING["loggers"]["mozilla_django_oidc"] = {
        "level": "INFO",
    }
