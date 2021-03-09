import unittest
from unittest import mock

import boto3

from alerts.sqs_queue import SQSQueue


class TestSQSQueue(unittest.TestCase):

    def test_post(self):
        mock_boto3_client = mock.MagicMock(boto3.session.Session.client)()
        sqs_queue = SQSQueue(
            queue_url='http://queue',
            client=mock_boto3_client
        )
        mock_boto3_client.send_message.return_value = {
            'ResponseMetadata': {'HTTPStatusCode': 200}
        }
        sqs_queue.post(message='test message')
        sqs_queue.client.send_message.assert_called_once_with(
            MessageBody='test message',
            QueueUrl='http://queue'
        )
