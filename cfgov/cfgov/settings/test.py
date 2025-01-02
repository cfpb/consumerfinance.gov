from .base import *


SECRET_KEY = "not-secret-key-for-testing"

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

# Disable caching for testing
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

ALLOW_ADMIN_URL = True

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

TEST_RUNNER = os.environ.get(
    "TEST_RUNNER", "core.testutils.runners.TestRunner"
)
ALWAYS_GENERATE_SLOW_REPORT = True

BAKER_CUSTOM_CLASS = "core.testutils.baker.ActualContentTypeBaker"

GOVDELIVERY_API = "core.govdelivery.MockGovDelivery"

# Disable Wagtail deletion archive storage during testing.
STORAGES.pop("wagtail_deletion_archival", None)

STATICFILES_FINDERS += [
    "core.testutils.mock_staticfiles.MockStaticfilesFinder",
]

STATICFILES_DIRS += [
    PROJECT_ROOT.joinpath("core", "testutils", "staticfiles"),
]

MOCK_STATICFILES_PATTERNS = {
    "icons/*.svg": "icons/placeholder.svg",
}

FLAG_SOURCES = ("flags.sources.SettingsFlagsSource",)

# We use a custom MEDIA_ROOT for testing so that tests that create images and
# other files don't write them to the local development media directory. The
# test runner cleans up this directory after the tests run.
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "cfgov", "tests", "test-media")

OPENSEARCH_DSL_AUTO_REFRESH = False
OPENSEARCH_DSL_AUTOSYNC = False

# Disable `use_ssl` for unit tests
OPENSEARCH_DSL["default"]["use_ssl"] = False


SKIP_DJANGO_MIGRATIONS = os.getenv("SKIP_DJANGO_MIGRATIONS", False)
if SKIP_DJANGO_MIGRATIONS:
    for _db in DATABASES.values():
        _db.setdefault("TEST", {})["MIGRATE"] = False

DEPLOY_ENVIRONMENT = "test"

INSTALLED_APPS += ("tccp.tests.testapp",)
