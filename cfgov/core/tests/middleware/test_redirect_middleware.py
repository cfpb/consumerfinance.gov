import csv
import re
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from core.middleware import RedirectMiddleware


def get_response(request):
    return HttpResponse("OK")


class TestRedirectMiddleware(SimpleTestCase):
    def setUp(self):
        self.middleware = RedirectMiddleware(get_response)

    def test_exact_match_permanent(self):
        request = RequestFactory().get("/retirement/")
        response = self.middleware(request)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"],
            "/consumer-tools/retirement/before-you-claim/",
        )

    def test_exact_match_case_insensitive(self):
        request = RequestFactory().get("/Retirement/")
        response = self.middleware(request)
        self.assertEqual(response.status_code, 301)

    def test_no_match_passes_through(self):
        request = RequestFactory().get("/this-does-not-exist/")
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")

    def test_regex_with_capture_group(self):
        request = RequestFactory().get("/payments/some-case/")
        response = self.middleware(request)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response["Location"],
            "/enforcement/payments-harmed-consumers/payments-by-case/some-case/",
        )

    def test_regex_blog_category(self):
        request = RequestFactory().get("/blog/category/mortgages/foo")
        response = self.middleware(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/about-us/blog/")

    def test_regex_no_match(self):
        request = RequestFactory().get("/not-a-pattern/")
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)


class TestRedirectMiddlewareCSVLoading(SimpleTestCase):
    def _make_middleware(self, filename, content):
        tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmpdir)
        path = Path(tmpdir)
        (path / filename).write_text(content, encoding="utf-8")

        patcher = patch.object(RedirectMiddleware, "CSV_DIR", new=path)
        patcher.start()
        self.addCleanup(patcher.stop)

        return RedirectMiddleware(get_response)

    @patch.object(RedirectMiddleware, "CSV_DIR", new=Path("/nonexistent/path"))
    def test_missing_csv_returns_empty(self):
        middleware = RedirectMiddleware(get_response)
        self.assertEqual(middleware._load_exact_redirects(), {})
        self.assertEqual(middleware._load_regex_redirects(), [])

    def test_load_exact_with_comments_and_blanks(self):
        middleware = self._make_middleware(
            "redirects.csv",
            "source_path,target_url,status_code\n"
            "# This is a comment\n"
            "\n"
            "/old/,/new/,301\n"
            "/temp/,/other/,302\n",
        )
        redirects = middleware._load_exact_redirects()
        self.assertEqual(len(redirects), 2)
        self.assertEqual(redirects["/old/"], ("/new/", 301))
        self.assertEqual(redirects["/temp/"], ("/other/", 302))

    def test_load_regex_converts_dollar_notation(self):
        middleware = self._make_middleware(
            "regex-redirects.csv",
            "pattern,target_url,status_code\n/old/(.*),/new/$1,301\n",
        )
        redirects = middleware._load_regex_redirects()
        self.assertEqual(len(redirects), 1)

        compiled, target_template, status = redirects[0]
        self.assertEqual(status, 301)
        m = compiled.match("/old/foo")
        self.assertTrue(m)
        self.assertEqual(m.expand(target_template), "/new/foo")


class TestCSVFileValidation(SimpleTestCase):
    """Validate the format of the actual redirect CSV files."""

    CSV_DIR = RedirectMiddleware.CSV_DIR

    def _iter_data_rows(self, filename):
        filepath = self.CSV_DIR / filename
        with filepath.open(encoding="utf-8") as f:
            reader = csv.reader(
                line
                for line in f
                if line.strip() and not line.strip().startswith("#")
            )
            header = next(reader)
            yield header
            yield from enumerate(reader, start=2)

    def test_exact_redirects_csv_format(self):
        rows = self._iter_data_rows("redirects.csv")
        header = next(rows)
        self.assertEqual(header, ["source_path", "target_url", "status_code"])

        for lineno, row in rows:
            with self.subTest(line=lineno):
                self.assertEqual(len(row), 3, f"expected 3 fields: {row}")
                source, target, status = [f.strip() for f in row]
                self.assertTrue(
                    source.startswith("/"),
                    f"source must start with /: {source}",
                )
                self.assertTrue(
                    target.startswith("/") or target.startswith("http"),
                    f"invalid target URL: {target}",
                )
                self.assertIn(int(status), (301, 302))

    def test_regex_redirects_csv_format(self):
        rows = self._iter_data_rows("regex-redirects.csv")
        header = next(rows)
        self.assertEqual(header, ["pattern", "target_url", "status_code"])

        for lineno, row in rows:
            with self.subTest(line=lineno):
                self.assertEqual(len(row), 3, f"expected 3 fields: {row}")
                pattern, target, status = [f.strip() for f in row]
                self.assertTrue(
                    pattern.startswith("/") or pattern.startswith("(/"),
                    f"pattern must start with /: {pattern}",
                )
                try:
                    re.compile(f"^{pattern}$")
                except re.error as e:
                    self.fail(f"invalid regex '{pattern}': {e}")
                self.assertTrue(
                    target.startswith("/")
                    or target.startswith("http")
                    or target.startswith("$"),
                    f"invalid target URL: {target}",
                )
                self.assertIn(int(status), (301, 302))
