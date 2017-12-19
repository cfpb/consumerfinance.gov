from __future__ import unicode_literals

import logging

from django.conf import settings
from django.test import RequestFactory, TestCase

from mock import patch


@patch('alerts.github_alert.GithubAlert.post')
class TestLoggingHandlers(TestCase):
    @classmethod
    def setUpClass(cls):
        """Replaces existing logging with CFGOVErrorHandler.

        Persists previous log configuration and global disable level. These
        then get restored in tearDownClass.
        """
        super(TestLoggingHandlers, cls).setUpClass()
        cls._logging = settings.LOGGING
        cls._logging_disable_level = logging.root.manager.disable

        logging.config.dictConfig({
            'version': 1,
            'handlers': {
                'cfgov': {
                    'level': 'ERROR',
                    'class': 'alerts.logging_handlers.CFGovErrorHandler',
                },
            },
            'loggers': {
                'testing': {
                    'handlers': ['cfgov'],
                    'level': 'ERROR',
                    'propagate': False,
                },
            },
        })
        logging.disable(logging.NOTSET)

        cls.logger = logging.getLogger('testing')

    @classmethod
    def tearDownClass(cls):
        """Restores regular logging."""
        logging.config.dictConfig(cls._logging)
        logging.disable(cls._logging_disable_level)
        super(TestLoggingHandlers, cls).tearDownClass()

    def test_logger_calls_github_api_post(self, github_api):
        self.logger.error('something')
        self.assertEqual(github_api.call_count, 1)

    def test_title_equals_message(self, github_api):
        message = 'error message with unic\xf3de characters'
        self.logger.error(message)
        args, kwargs = github_api.call_args
        self.assertEqual(kwargs['title'], message)

    def test_body_includes_message(self, github_api):
        message = 'error message with unic\xf3de characters'
        self.logger.error(message)
        args, kwargs = github_api.call_args
        self.assertIn(message, kwargs['body'])

    def test_body_includes_stack_trace_for_exception(self, github_api):
        try:
            raise ValueError('raising an exception')
        except ValueError:
            self.logger.exception('logging the exception')

        args, kwargs = github_api.call_args
        self.assertIn('Traceback (most recent call last)', kwargs['body'])

    def test_body_includes_exception_content(self, github_api):
        try:
            raise ValueError('raising an exception')
        except ValueError:
            self.logger.exception('logging the exception')

        args, kwargs = github_api.call_args
        self.assertIn('ValueError: raising an exception', kwargs['body'])

    def test_body_includes_request(self, github_api):
        request = RequestFactory().get('/')
        self.logger.error('something', extra={'request': request})

        args, kwargs = github_api.call_args
        self.assertIn('<WSGIRequest\npath:/', kwargs['body'])
