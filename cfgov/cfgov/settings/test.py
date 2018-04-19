from .local import *


# If a database wasn't defined in settings.base through the use of environment
# variables, default to using an in-memory SQLite one for unit tests.
#
# If a database is configured through environment settings, the unit tests will
# be run against a new test database on the same backend.
#
# See https://docs.djangoproject.com/en/dev/topics/testing/overview/#the-test-database
if not DATABASES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'TEST': {
                'NAME': ':memory:',
            },
        }
    }

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

TEST_RUNNER = 'cfgov.test.TestDataTestRunner'

INSTALLED_APPS += (
    'wagtail.contrib.settings',
    'wagtail.tests.testapp',
)

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.wagtailadmin.rich_text.HalloRichTextArea',
    },
    'custom': {
        'WIDGET': 'wagtail.tests.testapp.rich_text.CustomRichTextArea',
    },
}

GOVDELIVERY_API = 'core.govdelivery.MockGovDelivery'
