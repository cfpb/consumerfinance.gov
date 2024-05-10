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

STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
)

STATIC_ROOT = os.environ["DJANGO_STATIC_ROOT"]

# ALLOWED_HOSTS should be defined as a JSON list in the ALLOWED_HOSTS
# environment variable.
ALLOWED_HOSTS = environment_json(
    "ALLOWED_HOSTS",
    (
        "Environment variable ALLOWED_HOSTS is either not defined or is "
        "not valid JSON. Expected a JSON array of allowed hostnames."
    ),
)

# SSO Authentication
#
# Two abbreviations to note:
# - OP indicates the OIDC identity provider
# - RP indicates the OIDC relay provider, the client, this application
#
# Requires the following environment variables to be defined:
#
# - ENABLE_SSO: Enable SSO authentication with a value of "True".
# - OIDC_RP_CLIENT_ID: OIDC client identifier provided by the OP
# - OIDC_RP_CLIENT_SECRET: OIDC client secret provided by the OP
#
# Endpoints
# - OIDC_OP_BASE_URL: Base URL for all OP endpoitns
#
# Optional environment variables:
#
# - OIDC_RP_SIGN_ALGO: The algorithm used to sign ID tokens (default: HS256)
# - OIDC_RP_IDP_SIGN_KEY: The key (PEM) to sign ID tokens when
#                         OIDC_RP_SIGN_ALGO is RS256 (default: None)
#
# See the mozilla-django-oidc documentation for more details about the
# settings below:
# https://mozilla-django-oidc.readthedocs.io/en/stable/settings.html
ENABLE_SSO = os.environ.get("ENABLE_SSO") == "True"
if ENABLE_SSO:
    INSTALLED_APPS += ("mozilla_django_oidc",)
    AUTHENTICATION_BACKENDS += (
        "mozilla_django_oidc.auth.OIDCAuthenticationBackend",
    )
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    OIDC_RP_CLIENT_ID = os.environ["OIDC_RP_CLIENT_ID"]
    OIDC_RP_CLIENT_SECRET = os.environ["OIDC_RP_CLIENT_SECRET"]
    OIDC_RP_SIGN_ALGO = os.environ.get("OIDC_RP_SIGN_ALGO", "HS256")
    OIDC_RP_IDP_SIGN_KEY = os.environ.get("OIDC_RP_IDP_SIGN_KEY")
    OIDC_OP_BASE_URL = os.environ["OIDC_OP_BASE_URL"]

    OIDC_OP_AUTHORIZATION_ENDPOINT = f"{OIDC_OP_BASE_URL}/authorize"
    OIDC_OP_TOKEN_ENDPOINT = f"{OIDC_OP_BASE_URL}/token"
    OIDC_OP_USER_ENDPOINT = f"{OIDC_OP_BASE_URL}/userinfo"

    # Do not create users just-in-time. This will require users to be created
    # both in the IDP and the Django instance.
    OIDC_CREATE_USER = False

    LOGIN_URL = "oidc_authentication_init"
    LOGIN_REDIRECT_URL = reverse_lazy("wagtailadmin_home")
    LOGOUT_REDIRECT_URL = "/"

    LOGGING["loggers"]["mozilla_django_oidc"] = {
        "level": "DEBUG",
    }

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
SECURE_SSL_REDIRECT = True

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
