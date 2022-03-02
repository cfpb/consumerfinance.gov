import os

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings


@override_settings(
    STATICFILES_DIRS=[
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "staticfiles"
        ),
    ]
)
class MockStaticfilesFinderTests(TestCase):
    @override_settings(STATICFILES_FINDERS=[])
    def test_no_finders_test_file_not_found(self):
        """If there are no staticfiles finders, this file shouldn't be found.

        This test serves as a baseline to demonstrate the default behavior if
        Django has no staticfiles finders at all.
        """
        self.assertFalse(finders.find("icons/test.svg"))

    @override_settings(
        STATICFILES_FINDERS=[
            "django.contrib.staticfiles.finders.FileSystemFinder",
        ]
    )
    def test_filesystem_finder_finds_test_file(self):
        """If the FileSystemFinder is used, the file should be found.

        The whole test case has been decorated with a STATICFILES_DIRS path
        that contains an icons/test.svg file. If we add the FileSystemFinder to
        the list of staticfiles finders, this file should be found.

        This test serves as a baseline to demonstrate default Django behavior.
        """
        self.assertRegex(finders.find("icons/test.svg"), "icons/test.svg$")

    @override_settings(
        STATICFILES_FINDERS=[
            "core.testutils.mock_staticfiles.MockStaticfilesFinder",
        ]
    )
    def test_mock_finder_no_setting_raises_improperlyconfigured(self):
        """MockStaticfilesFinder requires the presence of a certain setting."""
        del settings.MOCK_STATICFILES_PATTERNS
        with self.assertRaises(ImproperlyConfigured):
            finders.find("icons/test.svg")

    @override_settings(
        STATICFILES_FINDERS=[
            "core.testutils.mock_staticfiles.MockStaticfilesFinder",
        ],
        MOCK_STATICFILES_PATTERNS=("this", "should", "be", "a", "dict"),
    )
    def test_mock_finder_invalid_setting_raises_improperlyconfigured(self):
        """MockStaticfilesFinder needs its setting to be a dict."""
        with self.assertRaises(ImproperlyConfigured):
            finders.find("icons/test.svg")

    @override_settings(
        STATICFILES_FINDERS=[
            "core.testutils.mock_staticfiles.MockStaticfilesFinder",
        ],
        MOCK_STATICFILES_PATTERNS={
            "missing/*.svg": "icons/test.svg",
        },
    )
    def test_mock_finder_only_test_file_not_found(self):
        """If only MockStaticfilesFinder is used, the file should not be found.

        Here we use the MockStaticfilesFinder, and tell it how to route a
        request for missing/file.svg, but we haven't also enabled the Django
        FileSystemFinder. So there are no other finders to locate the
        icons/test.svg that the mock finder is redirecting to, and we expect
        this call to fail.
        """
        self.assertFalse(finders.find("missing/file.svg"))

    @override_settings(
        STATICFILES_FINDERS=[
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "core.testutils.mock_staticfiles.MockStaticfilesFinder",
        ],
        MOCK_STATICFILES_PATTERNS={
            "missing/*.svg": "icons/test.svg",
        },
    )
    def test_mock_finder_falls_back_to_filesystem_finder(self):
        """If both finders are defined, the request should succeed.

        We expect the MockStaticfilesFinder to handle the request for
        missing/file.svg and redirect it to any other finders for
        icons/test.svg instead. Because we have a FileSystemFinder that can
        handle that redirected request, this call should succeed.
        """
        self.assertRegex(finders.find("missing/file.svg"), "icons/test.svg$")

    @override_settings(
        STATICFILES_FINDERS=[
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "core.testutils.mock_staticfiles.MockStaticfilesFinder",
        ],
        MOCK_STATICFILES_PATTERNS={
            "missing/*.svg": "icons/test.svg",
        },
    )
    def test_no_match_if_pattern_doesnt_match_input(self):
        """If a request is made that no finder can handle, it should fail.

        Even if both finders are enabled, requests should fail if there are no
        finders that can locate the requested file.
        """
        self.assertFalse(finders.find("does-not-exist"))
