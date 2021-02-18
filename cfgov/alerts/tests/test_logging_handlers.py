import logging
import os
from unittest.mock import patch

from django.conf import settings
from django.http import QueryDict
from django.test import RequestFactory, TestCase


class ObjectThatCantBeRepresented(object):
    def __repr__(self):
        raise Exception


@patch('alerts.sqs_queue.SQSQueue.post')
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

        credentials = {
            'AWS_SQS_QUEUE_URL': 'test-queue',
            'AWS_SQS_ACCESS_KEY_ID': 'access-key',
            'AWS_SQS_SECRET_ACCESS_KEY': 'secret-key',
        }

        with patch.dict(os.environ, credentials):
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

    def test_logger_calls_sqs_queue_post(self, sqs_queue_post):
        self.logger.error('something')
        self.assertEqual(sqs_queue_post.call_count, 1)

    def test_body_includes_message(self, sqs_queue_post):
        message = 'error message with unic\xf3de characters'
        self.logger.error(message)
        args, kwargs = sqs_queue_post.call_args
        self.assertIn(message, kwargs['message'])

    def test_body_includes_stack_trace_for_exception(self, sqs_queue_post):
        try:
            raise ValueError('raising an exception')
        except ValueError:
            self.logger.exception('logging the exception')

        args, kwargs = sqs_queue_post.call_args
        self.assertIn('Traceback (most recent call last)', kwargs['message'])

    def test_body_includes_exception_content(self, sqs_queue_post):
        try:
            raise ValueError('raising an exception')
        except ValueError:
            self.logger.exception('logging the exception')

        args, kwargs = sqs_queue_post.call_args
        self.assertIn('ValueError: raising an exception', kwargs['message'])

    def test_body_includes_request_if_provided(self, sqs_queue_post):
        request = RequestFactory().get('/')
        self.logger.error('something', extra={'request': request})

        args, kwargs = sqs_queue_post.call_args
        self.assertIn(
            'Request repr(): \n<WSGIRequest\npath:/',
            kwargs['message']
        )

    def test_body_shows_none_if_no_request_available(self, sqs_queue_post):
        self.logger.error('something')

        args, kwargs = sqs_queue_post.call_args
        self.assertIn('Request repr(): \nNone', kwargs['message'])

    def test_body_handles_unparseable_querydict(self, sqs_queue_post):
        """Handle when calls to format request.GET or POST fail."""
        with patch.object(QueryDict, '__repr__', side_effect=Exception):
            request = RequestFactory().get('/')
            self.logger.error('something', extra={'request': request})

        args, kwargs = sqs_queue_post.call_args
        self.assertIn('<could not parse>', kwargs['message'])

    def test_body_handles_unparseable_dict(self, sqs_queue_post):
        """Handle when calls to format request.COOKIES or META fail."""
        request = RequestFactory().get('/')
        request.COOKIES = {'test': ObjectThatCantBeRepresented()}
        request.META = {'test': ObjectThatCantBeRepresented()}
        self.logger.error('something', extra={'request': request})

        args, kwargs = sqs_queue_post.call_args
        self.assertIn('<could not parse>', kwargs['message'])

    def test_body_handles_request_with_invalid_post(self, sqs_queue_post):
        """Handle case when a request was generated with an invalid POST."""
        request = RequestFactory().post('/')
        request._post = {'test': ObjectThatCantBeRepresented()}
        self.logger.error('something', extra={'request': request})

        args, kwargs = sqs_queue_post.call_args
        self.assertIn('<could not parse>', kwargs['message'])
