import csv
import re
from pathlib import Path

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.middleware.csrf import CsrfViewMiddleware
from django.shortcuts import redirect
from django.utils import translation
from django.utils.encoding import force_str

from wagtail.rich_text import expand_db_html

from core.utils import add_link_markup, get_body_html, get_link_tags


class DownstreamCacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if "CSRF_COOKIE_USED" in request.META:
            response["Edge-Control"] = "no-store"

        return response


def parse_links(html, request_path=None, encoding=None):
    """Process all links in given html and replace them if markup is added."""
    if encoding is None:
        encoding = settings.DEFAULT_CHARSET

    # The passed HTML may be a string or bytes, depending on what is calling
    # this method. For example, Django response.content is always bytes. We
    # always want this content to be a string for our purposes.
    html_as_text = force_str(html, encoding=encoding)

    # This call invokes Wagtail-specific logic that converts references to
    # Wagtail pages, documents, and images to their proper link URLs.
    expanded_html = expand_db_html(html_as_text)

    # Parse links only in the <body> of the HTML
    body_html = get_body_html(expanded_html)
    if body_html is None:
        return expanded_html

    link_tags = get_link_tags(body_html)
    for tag in link_tags:
        tag_with_markup = add_link_markup(tag, request_path)
        if tag_with_markup:
            expanded_html = expanded_html.replace(tag, tag_with_markup)

    return expanded_html


class ParseLinksMiddleware:
    response_flag = "links_parsed"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if self.should_parse_links(request, response):
            response.content = parse_links(
                response.content, request.path, encoding=response.charset
            )
            setattr(response, self.response_flag, True)
        return response

    @classmethod
    def should_parse_links(cls, request, response):
        """Determine if links should be parsed for a given request/response.

        Returns True if

        1. The response hasn't had this middleware applied before AND
        2. The response has the settings.DEFAULT_CONTENT_TYPE (HTML) AND
        3. The request path does not match settings.PARSE_LINKS_EXCLUSION_LIST

        Otherwise returns False.
        """
        if hasattr(response, cls.response_flag):
            return False

        if "html" not in response.get("Content-Type", ""):
            return False

        return not any(
            re.search(regex, request.path)
            for regex in settings.PARSE_LINKS_EXCLUSION_LIST
        )


class DeactivateTranslationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        translation.deactivate()
        return response


class SelfHealingMiddleware:
    """Attempt to self-heal 404-ing URLs.
    Takes a 404ing request and tries to transform it to a successful request
    by lowercasing the path and stripping extraneous characters from the end.
    If those result in a modified path, redirect to the modified path.
    If the path did not change, this is a legitimate 404, so continue handling
    that as normal.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If this request isn't 404ing, just return the existing response.
        if response.status_code != 404:
            return response

        # Lowercase the path.
        path = request.path.lower()

        # Check for and remove extraneous characters at the end of the path.
        extraneous_char_re = re.compile(
            r'[`~!@#$%^&*()\-_–—=+\[\]{}\\|;:\'‘’"“”,.…<>? ]+$'
        )
        path = extraneous_char_re.sub("", path)

        # If the path has changed, redirect to the new path.
        if path != request.path:
            return redirect(path, permanent=True)

        return response


class PathBasedCsrfViewMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        csrf_required_paths = getattr(settings, "CSRF_REQUIRED_PATHS", None)

        # If CSRF_REQUIRED_PATHS is not configured, apply the CSRF middleware
        # to everything. Otherwise only apply it if the request path matches
        # the configured paths.
        if csrf_required_paths is not None and not any(
            request.path.startswith(path) for path in csrf_required_paths
        ):
            return None

        return super().process_view(
            request, callback, callback_args, callback_kwargs
        )


class RedirectMiddleware:
    """Handle redirects defined in CSV files.

    Loads exact-match redirects from redirects.csv and regular expression
    redirects from regex_redirects.csv.
    """

    CSV_DIR = Path(__file__).resolve().parent

    # Regex redirect targets can look like /path/$1 or /path{1}123
    # for cases where the target has a number next to the substitution.
    CAPTURE_GROUP_RE = re.compile(r"\$\{(\d+)\}|\$(\d+)")

    def __init__(self, get_response):
        self.get_response = get_response
        self.exact_redirects = self._load_exact_redirects()
        self.regex_redirects = self._load_regex_redirects()

    def _read_csv(self, filename):
        """Read redirects from a CSV.

        Expected format: from_path,to_url,status_code

        from_path should not have a leading slash.
        """
        filepath = self.CSV_DIR / filename

        if not filepath.exists():
            return []

        with filepath.open(encoding="utf-8") as f:
            reader = csv.reader(
                line
                for line in f
                if line.strip() and not line.strip().startswith("#")
            )
            next(reader, None)  # Skip header row

            return [
                (row[0].strip(), row[1].strip(), int(row[2].strip()))
                for row in reader
            ]

    def _load_exact_redirects(self):
        """Load basic path-based redirects from redirects.csv.

        Expected format: redirect_from,redirect_to,status_code

        Our SelfHealingMiddleware (above) always tries lowercasing request
        paths, so we can similarly lowercase our redirect sources.

        Returns {redirect_from: (redirect_to, status_code)}.
        """
        return {
            source.lower(): (target, status)
            for source, target, status in self._read_csv("redirects.csv")
        }

    def _load_regex_redirects(self):
        """Load regex redirects from regex-redirects.csv

        Expected format: redirect_from_pattern,redirect_to,status_code

        redirect_from may have capture groups: /path/from/(.*)

        redirect_to may use those groups /redirected/to/$1 or
        /redirected/to/${1}123 for cases where the destination URL has digits
        adjacent to the substituted text.

        Returns list of (from_pattern, redirect_to_template, status_code).
        """
        return [
            (
                re.compile(f"^{pattern}$", re.IGNORECASE),
                self.CAPTURE_GROUP_RE.sub(
                    lambda m: f"\\g<{m.group(1) or m.group(2)}>", target
                ),
                status_code,
            )
            for pattern, target, status_code in self._read_csv(
                "regex-redirects.csv"
            )
        ]

    def _redirect(self, url, status_code):
        if status_code == 301:
            return HttpResponsePermanentRedirect(url)
        return HttpResponseRedirect(url)

    def __call__(self, request):
        path = request.path

        # Try exact match first.
        match = self.exact_redirects.get(path.lower())

        if match:
            return self._redirect(*match)

        # Try regex patterns next.
        for compiled, target_template, status_code in self.regex_redirects:
            regex_match = compiled.match(path)

            if regex_match:
                return self._redirect(
                    regex_match.expand(target_template), status_code
                )

        # No redirects match, continue with regular request handling.
        return self.get_response(request)
