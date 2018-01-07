from .local import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(REPOSITORY_ROOT, 'db.sqlite3'),
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
