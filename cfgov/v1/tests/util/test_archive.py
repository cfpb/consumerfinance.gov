from django.test import SimpleTestCase, override_settings

from v1.util.archive import url_in_archive


@override_settings(ARCHIVE_BASE_PATH="/test-archive/")
class URLInArchiveTests(SimpleTestCase):
    def test_valid_cases(self):
        for url in [
            "/test-archive/",
            "/test-archive/page/",
            "/test-archive/page/?query=1",
            "https://www.consumerfinance.gov/test-archive/",
            "https://www.other.com/test-archive/foo/",
        ]:
            with self.subTest(url=url):
                self.assertTrue(url_in_archive(url))

    def test_invalid_cases(self):
        for url in [
            "test-archive",
            "test-archive/",
            "/foo/bar/",
            "/foo/bar/test-archive/",
        ]:
            with self.subTest(url=url):
                self.assertFalse(url_in_archive(url))
