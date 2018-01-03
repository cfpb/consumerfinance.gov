import unittest

import boto3
import mock

from alerts.send_new_relic_messages_to_sqs import (
    cache_known_violations, read_known_violations, send_violations
)


class TestSendNewRelicMessagesToSQS(unittest.TestCase):

    def test_cache_known_violations(self):
        with mock.patch('__builtin__.open', create=True) as mock_open:
            mock_open.return_value = mock.MagicMock(spec=file)
            cache_known_violations('/some/file.json', [12345, '23456'])

        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.writelines.assert_called_with(['12345\n', '23456\n'])

    def test_read_known_violations_existing(self):
        with mock.patch('__builtin__.open', create=True) as mock_open:
            mock_open.return_value = mock.MagicMock(spec=file)
            file_handle = mock_open.return_value.__enter__.return_value
            file_handle.readlines.return_value = ['12345\n', '23456\n']
            known_violations = read_known_violations('/some/file.json')

        self.assertEqual([12345, 23456], known_violations)

    def test_read_known_violations_nonexisting(self):
        with mock.patch('__builtin__.open', create=True) as mock_open:
            mock_open.side_effect = IOError()
            known_violations = read_known_violations('/some/file.json')
        self.assertEqual([], known_violations)

    def test_send_violations(self):
        mock_boto3_client = mock.MagicMock(boto3.session.Session.client)()
        mock_boto3_client.send_message.return_value = {
            'ResponseMetadata': {'HTTPStatusCode': 200}
        }
        send_violations(mock_boto3_client,
                        'http://queue',
                        ['test violation message'])
        mock_boto3_client.send_message.assert_called_once_with(
            MessageBody='test violation message',
            QueueUrl='http://queue')

    def test_send_violations_not200(self):
        mock_boto3_client = mock.MagicMock(boto3.session.Session.client)()
        mock_boto3_client.send_message.return_value = {
            'ResponseMetadata': {'HTTPStatusCode': 400}
        }
        with self.assertRaises(SystemExit):
            send_violations(mock_boto3_client,
                            'http://queue',
                            ['test violation message'])

    def test_send_violations_dryrun(self):
        mock_boto3_client = mock.MagicMock(boto3.session.Session.client)()
        send_violations(mock_boto3_client,
                        'http://queue',
                        ['test violation message'],
                        dryrun=True)
        mock_boto3_client.send_message.assert_not_called()
