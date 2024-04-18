import os
import sys
from os.path import exists

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.utils.text import format_lazy

import saml2

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

# SAML2 Authentication
#
# Requires the SAML_AUTH, SAML_ROOT_URL, SAML_ENTITY_ID, and SAML_METADATA_URL
# environment variables to be defined.
#
# - SAML_AUTH: Enable SAML2 authentication with a value of "True".
# - SAML_ROOT_URL: The URL that browsers will use to access this site. The
#   SAML2 relay URL will be constructed from this, and it must match what is
#   configured for this site in the SAML2 identity provider.
# - SAML_ENTITY_ID: The entity id configured for this service provider in the
#   SAML2 identity provider.
# - SAML_METADATA_URL: The remote URL of the identity provider's metadata for
#   this service provider.
#
# See the djangosaml2 documentation at
# https://djangosaml2.readthedocs.io/contents/setup.html#configuration
# and the pySAML2 documentation at https://pysaml2.readthedocs.io/
# for more details about the configuration below.
SAML_AUTH = os.environ.get("SAML_AUTH") == "True"
if SAML_AUTH:
    # Update built-in Django settings for SAML authetnication
    INSTALLED_APPS += ("djangosaml2",)
    MIDDLEWARE += ("djangosaml2.middleware.SamlSessionMiddleware",)
    AUTHENTICATION_BACKENDS += ("djangosaml2.backends.Saml2Backend",)
    LOGIN_URL = "/saml2/login/"
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

    # Map Django attributes to our SAML identity provider
    SAML_DJANGO_USER_MAIN_ATTRIBUTE = "email"
    SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP = "__iexact"
    SAML_ATTRIBUTE_MAPPING = {
        "emailAddress": ("email",),
    }
    SAML_CREATE_UNKNOWN_USER = False

    # URL lookups
    SAML_ROOT_URL = os.environ["SAML_ROOT_URL"]
    ACS_URL = format_lazy(
        "{root_url}{acs_path}",
        root_url=SAML_ROOT_URL,
        acs_path=reverse_lazy("saml2_acs"),
    )
    ACS_DEFAULT_REDIRECT_URL = reverse_lazy("wagtailadmin_home")

    # Configure PySAML2 for our identity provider
    SAML_CONFIG = {
        "debug": DEBUG,
        "xmlsec_binary": "/usr/bin/xmlsec1",
        "entityid": os.environ["SAML_ENTITY_ID"],
        "metadata": {
            "remote": [{"url": os.environ["SAML_METADATA_URL"]}],
        },
        "service": {
            "sp": {
                "endpoints": {
                    "assertion_consumer_service": [
                        (ACS_URL, saml2.BINDING_HTTP_REDIRECT),
                        (ACS_URL, saml2.BINDING_HTTP_POST),
                    ],
                },
                "allow_unsolicited": True,
                "authn_requests_signed": False,
                "logout_requests_signed": True,
                "want_assertions_signed": True,
                "want_response_signed": False,
            },
        },
    }

    # Add logging
    LOGGING["loggers"]["saml2"] = {
        "level": "INFO",
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
