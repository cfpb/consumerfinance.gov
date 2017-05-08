from .test_nomigrations import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db.sqlite3',
        'TEST': {
            'NAME': ':memory:',
        }
    },
}

TEST_RUNNER = 'cfgov.test.AcceptanceTestRunner'
