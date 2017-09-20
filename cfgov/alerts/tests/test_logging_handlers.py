# -*- coding: utf-8 -*-

from django.test import TestCase
from mock import patch, MagicMock

from alerts.logging_handlers import CFGovErrorHandler


class TestLoggingHandlers(TestCase):

    @patch('alerts.github_alert.GithubAlert.post')
    def test_emit(self, github_alert):
        """ Test that calling CFGOVErrorHandler.emit
        makes a GithubAlert post with the right parameters
        """
        message = u'Internal Server Error: /tést'
        exc_text = ('Traceback (most recent call last)'
                    'TypeError: NoneType object has no attribute __getitem__')
        record = MagicMock(
            message=message,
            exc_text=exc_text,
        )
        CFGovErrorHandler().emit(record)
        github_alert.assert_called_once_with(
            title=message,
            body=exc_text,
        )
