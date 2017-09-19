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
        message = (u'Internal Server Error: /tést-page/'
                   'Traceback (most recent call last):'
                   '... more details ...')
        record = MagicMock(message=message)
        CFGovErrorHandler().emit(record)
        github_alert.assert_called_once_with(
            title=message[:30],
            body=message,
        )
