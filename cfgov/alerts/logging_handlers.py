from __future__ import unicode_literals

import logging
import os

from django.utils.encoding import force_text
from django.views.debug import get_exception_reporter_filter

from alerts.sqs_queue import SQSQueue


class CFGovErrorHandler(logging.Handler):
    """Logging handler that posts errors to our SQS queue.

    Based on django.utils.log.AdminEmailHandler.

    Generated GitHub issues include all of the same information that Django
    admin emails do. Details at:

    https://docs.djangoproject.com/en/1.8/howto/error-reporting/#filtering-sensitive-information
    """

    def __init__(self):
        logging.Handler.__init__(self)
        self.sqs_queue = SQSQueue(
            queue_url=os.environ['AWS_SQS_QUEUE_URL'],
            credentials={
                'access_key': os.environ['AWS_SQS_ACCESS_KEY_ID'],
                'secret_key': os.environ['AWS_SQS_SECRET_ACCESS_KEY'],
            }
        )

    def emit(self, record):
        title = self.format_title(record)
        body = self.format_body(record)
        message = '{title} - {body}'.format(title=title, body=body)
        self.sqs_queue.post(message=message)

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
