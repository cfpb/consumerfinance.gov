from .local import *


# A test database may be specified through use of the TEST_DATABASE_URL
# environment variable. If not provided, unit tests will be run against an
# in-memory SQLite database.
TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')
if TEST_DATABASE_URL:
    TEST_DATABASE = dj_database_url.parse(TEST_DATABASE_URL)
else:
    TEST_DATABASE = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {
            'NAME': ':memory:',
        },
    }

DATABASES = {'default': TEST_DATABASE}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

TEST_RUNNER = os.environ.get('TEST_RUNNER', 'cfgov.test.TestRunner')

INSTALLED_APPS += (
    'wagtail.contrib.settings',
    'wagtail.tests.testapp',
)

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.HalloRichTextArea',
    },
    'custom': {
        'WIDGET': 'wagtail.tests.testapp.rich_text.CustomRichTextArea',
    },
}

GOVDELIVERY_API = 'core.govdelivery.MockGovDelivery'

STATICFILES_FINDERS += [
    'core.testutils.mock_staticfiles.MockStaticfilesFinder',
]

STATICFILES_DIRS += [
    PROJECT_ROOT.child('core', 'testutils', 'staticfiles'),
]

MOCK_STATICFILES_PATTERNS = {
    'icons/*.svg': 'icons/placeholder.svg',
}

FLAG_SOURCES = (
    'flags.sources.SettingsFlagsSource',
)

# We use a custom MEDIA_ROOT for testing so that tests that create images and
# other files don't write them to the local development media directory. The
# test runner cleans up this directory after the tests run.
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'cfgov', 'tests', 'test-media')
