from .test_nomigrations import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {
            'NAME': ':memory:',
        }
    },
}

TEST_RUNNER = 'cfgov.test.AcceptanceTestRunner'
