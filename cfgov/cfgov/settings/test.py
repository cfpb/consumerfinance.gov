from .local import *


EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

TEST_RUNNER = os.environ.get(
    'TEST_RUNNER',
    'core.testutils.runners.TestRunner'
)

BAKER_CUSTOM_CLASS = 'core.testutils.baker.ActualContentTypeBaker'

INSTALLED_APPS += (
    'wagtail.contrib.settings',
    'wagtail.tests.testapp',
)

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
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

# Use a test-specific index
HAYSTACK_CONNECTIONS["default"]["INDEX_NAME"] = (
    "test_" + HAYSTACK_CONNECTIONS["default"]["INDEX_NAME"]
)
