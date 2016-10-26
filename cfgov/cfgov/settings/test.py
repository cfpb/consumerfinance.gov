from .local import *

HTML_MINIFY = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(REPOSITORY_ROOT, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

TEST_RUNNER = 'cfgov.test.TestDataTestRunner'

LOGGING = {}

INSTALLED_APPS += (
    'wagtail.tests.testapp',
)
