from .base import *


DEBUG = True
ALLOW_ADMIN_URL = True
SECRET_KEY = "not-secret-key-for-testing"

INSTALLED_APPS += (
    "sslserver",
    "wagtail.contrib.styleguide",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        }
    },
}

# Log database queries
if os.environ.get("ENABLE_SQL_LOGGING"):
    LOGGING["loggers"]["django.db.backends"] = {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": False,
    }

# Log Elasticsearch queries
if os.environ.get("ENABLE_ES_LOGGING"):
    LOGGING["loggers"]["elasticsearch.trace"] = {
        "handlers": ["console"],
        "level": "INFO",
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

# Disable caching unless enabled via environment variable
if not os.getenv("ENABLE_DEFAULT_CACHE"):
    CACHES["default"] = {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }

# Use a mock GovDelivery API instead of the real thing,
# unless the GOVDELIVERY_BASE_URL environment variable is set.
if not os.environ.get("GOVDELIVERY_BASE_URL"):
    GOVDELIVERY_API = "core.govdelivery.LoggingMockGovDelivery"

# Use a placeholder image service to replace images that are uploaded to S3
_placeholder_domain = "dummyimage.com"
WAGTAIL_PLACEHOLDERIMAGES_DUMMY = True
WAGTAIL_PLACEHOLDERIMAGES_SOURCE = (
    f"//{_placeholder_domain}/{{width}}x{{height}}/addc91/1fa040"
)

CSP_IMG_SRC += (_placeholder_domain,)

# Add django-cprofile-middleware to enable lightweight local profiling.
# The middleware's profiling is only available if DEBUG=True
MIDDLEWARE += ("django_cprofile_middleware.middleware.ProfilerMiddleware",)
DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False

# If DEPLOY_ENVIRONMENT hasn't been set by the environment in base.py,
# default it to local.
DEPLOY_ENVIRONMENT = DEPLOY_ENVIRONMENT or "local"

# Disable use_ssl for functional tests
OPENSEARCH_DSL["default"]["use_ssl"] = False