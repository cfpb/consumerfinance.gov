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
    k: {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "TIMEOUT": 0,
    }
    for k in ("default", "post_preview")
}

ALLOW_ADMIN_URL = True

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

TEST_RUNNER = os.environ.get(
    "TEST_RUNNER", "core.testutils.runners.TestRunner"
)

BAKER_CUSTOM_CLASS = "core.testutils.baker.ActualContentTypeBaker"

INSTALLED_APPS += (
    "wagtail.contrib.settings",
    "wagtail.test.snippets",
    "wagtail.test.testapp",
)

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "h2",
                "h3",
                "h4",
                "h5",
                "blockquote",
                "hr",
                "ol",
                "ul",
                "bold",
                "italic",
                "link",
                "document-link",
                "image",
            ]
        },
    },
    "custom": {
        "WIDGET": "wagtail.test.testapp.rich_text.CustomRichTextArea",
    },
}

GOVDELIVERY_API = "core.govdelivery.MockGovDelivery"

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

if os.getenv("SKIP_DJANGO_MIGRATIONS"):

    class _NoMigrations:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = _NoMigrations()

DEPLOY_ENVIRONMENT = "test"

# Axes requires a request for authentication, which breaks uses of Django's
# test client .login() method. This disables it when running tests.
AXES_ENABLED = False
