import logging
import os
from pprint import pformat

from django.utils.encoding import force_str
from django.views.debug import get_exception_reporter_filter

from alerts.sqs_queue import SQSQueue


class CFGovErrorHandler(logging.Handler):
    """Logging handler that posts errors to our SQS queue.

    Based on django.utils.log.AdminEmailHandler.

    Generated GitHub issues include stack trace and request information.
    Sensitive request POST parameters are filtered using this Django logic:

    https://docs.djangoproject.com/en/stable/howto/error-reporting/#filtering-sensitive-information
    """

    def __init__(self):
        logging.Handler.__init__(self)
        self.sqs_queue = SQSQueue(
            queue_url=os.environ["AWS_SQS_QUEUE_URL"],
            credentials={
                "access_key": os.environ["AWS_SQS_ACCESS_KEY_ID"],
                "secret_key": os.environ["AWS_SQS_SECRET_ACCESS_KEY"],
            },
        )

    def emit(self, record):
        title = self.format_title(record)
        body = self.format_body(record)
        message = "{title} - {body}".format(title=title, body=body)
        self.sqs_queue.post(message=message)

    def format_title(self, record):
        return record.getMessage()

    def format_body(self, record):
        try:
            request = record.request
        except AttributeError:
            request = None

        return "%s\n\nRequest repr(): \n%s" % (
            self.format(record),
            self._get_request_repr(request),
        )

    def _get_request_repr(self, request):
        """
        Generates a text representation of a Django request for use in logging
        500 errors.

        Copy of django.views.debug.ExceptionReporterFilter.get_request_repr,
        removed in Django 1.9:

        https://github.com/django/django/blob/1.8.19/django/views/debug.py#L118
        https://docs.djangoproject.com/en/dev/releases/1.9/#httprequest-details-in-error-reporting

        Copied here to maintain existing behavior on upgrade to Django 1.11.

        Slightly modified to encapsulate logic around null requests.
        """
        if request is None:
            return repr(None)

        filter = get_exception_reporter_filter(request)
        post_override = filter.get_post_parameters(request)

        return self._build_request_repr(request, post_override)

    def _build_request_repr(self, request, POST_override):
        """
        Builds and returns the request's representation string. The request's
        attributes may be overridden by pre-processed values.

        Copy of django.http.request.build_request_repr, removed in Django 1.9:

        https://github.com/django/django/blob/1.8.19/django/http/request.py#L468
        https://docs.djangoproject.com/en/dev/releases/1.9/#httprequest-details-in-error-reporting

        Copied here to maintain existing behavior on upgrade to Django 1.11.

        This code has been simplified to accept a single required parameter for
        overriding POST parameters. The original code makes this parameter
        optional and supports other arguments which are not used anywhere.
        """
        # Since this is called as part of error handling, we need to be very
        # robust against potentially malformed input.
        try:
            get = pformat(request.GET)
        except Exception:
            get = "<could not parse>"

        try:
            post = pformat(POST_override)
        except Exception:
            post = "<could not parse>"

        try:
            cookies = pformat(request.COOKIES)
        except Exception:
            cookies = "<could not parse>"

        try:
            meta = pformat(request.META)
        except Exception:
            meta = "<could not parse>"

        path = request.path

        return force_str(
            "<%s\npath:%s,\nGET:%s,\nPOST:%s,\nCOOKIES:%s,\nMETA:%s>"
            % (
                request.__class__.__name__,
                path,
                str(get),
                str(post),
                str(cookies),
                str(meta),
            )
        )
