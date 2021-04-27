import sys
import warnings

import django

from .base import *


if sys.version_info[0] < 3:
    raise Exception(
        "Python 2 is no longer supported. "
        "If you are running in a virtual environment, please see "
        "http://cfpb.github.io/consumerfinance.gov/running-virtualenv/"
        "#reinstalling-the-virtual-environment "
        "for how to reinstall."
    )

DEBUG = True
SECRET_KEY = "not-secret-key-for-testing"

INSTALLED_APPS += (
    "sslserver",
    "wagtail.contrib.styleguide",
)

STATIC_ROOT = REPOSITORY_ROOT.joinpath("collectstatic")

ALLOW_ADMIN_URL = DEBUG or os.environ.get("ALLOW_ADMIN_URL", False)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler",}
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO", "propagate": True,}
    },
}

# Log database queries
if os.environ.get("ENABLE_SQL_LOGGING"):
    LOGGING["loggers"]["django.db.backends"] = {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": False,
    }

# Django Debug Toolbar
if os.environ.get("ENABLE_DEBUG_TOOLBAR"):
    INSTALLED_APPS += ("debug_toolbar",)

    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "flags.panels.FlagsPanel",
        "flags.panels.FlagChecksPanel",
    ]

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_COLLAPSED": True,
        "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
    }

MIDDLEWARE += CSP_MIDDLEWARE

# Disable caching when working locally
CACHES = {
    k: {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "TIMEOUT": 0,
    }
    for k in ("default", "post_preview")
}

# Optionally enable cache for post_preview
if os.environ.get("ENABLE_POST_PREVIEW_CACHE"):
    CACHES["post_preview"] = {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "post_preview_cache",
        "TIMEOUT": None,
    }

# Use a mock GovDelivery API instead of the real thing,
# unless the GOVDELIVERY_BASE_URL environment variable is set.
if not os.environ.get("GOVDELIVERY_BASE_URL"):
    GOVDELIVERY_API = "core.govdelivery.LoggingMockGovDelivery"

# Use a placeholder image service to replace images that are uploaded to S3
WAGTAIL_PLACEHOLDERIMAGES_DUMMY = True
WAGTAIL_PLACEHOLDERIMAGES_SOURCE = "//placekitten.com/{width}/{height}"

CSP_IMG_SRC += (
    "placekitten.com",
)

ELASTICSEARCH_SYNONYMS_HOME = './search/resources'

# Add django-cprofile-middleware to enable lightweight local profiling.
# The middleware's profiling is only available if DEBUG=True
MIDDLEWARE += ("django_cprofile_middleware.middleware.ProfilerMiddleware",)
DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False
