import logging

from django.utils.encoding import force_text
from django.views.debug import get_exception_reporter_filter

from alerts.github_alert import GithubAlert


class CFGovErrorHandler(logging.Handler):
    """Logging handler that posts errors to GitHub.

    Based on django.utils.log.AdminEmailHandler.

    Generated GitHub issues include all of the same information that Django
    admin emails do. Details at:

    https://docs.djangoproject.com/en/1.8/howto/error-reporting/#filtering-sensitive-information
    """
    def emit(self, record):
        title = self.format_title(record)
        body = self.format_body(record)

        github_api = GithubAlert(credentials={})
        github_api.post(title=title, body=body)

    def format_title(self, record):
        return record.getMessage()

    def format_body(self, record):
        try:
            request = record.request
            filter = get_exception_reporter_filter(request)
            request_repr = '\n{}'.format(
                force_text(filter.get_request_repr(request))
            )
        except Exception:
            request = None
            request_repr = "unavailable"

        return "%s\n\nRequest repr(): %s" % (self.format(record), request_repr)
