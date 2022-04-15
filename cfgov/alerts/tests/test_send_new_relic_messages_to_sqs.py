import unittest
from io import TextIOBase
from unittest import mock

from alerts.send_new_relic_messages_to_sqs import (
    cache_known_violations,
    read_known_violations,
)


class TestSendNewRelicMessagesToSQS(unittest.TestCase):
    def test_cache_known_violations(self):
        with mock.patch("builtins.open", create=True) as mock_open:
            mock_open.return_value = mock.MagicMock(spec=TextIOBase)
            cache_known_violations("/some/file.json", [12345, "23456"])

        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.writelines.assert_called_with(["12345\n", "23456\n"])

    def test_read_known_violations_existing(self):
        with mock.patch("builtins.open", create=True) as mock_open:
            mock_open.return_value = mock.MagicMock(spec=TextIOBase)
            file_handle = mock_open.return_value.__enter__.return_value
            file_handle.readlines.return_value = ["12345\n", "23456\n"]
            known_violations = read_known_violations("/some/file.json")

        self.assertEqual([12345, 23456], known_violations)

    def test_read_known_violations_nonexisting(self):
        with mock.patch("builtins.open", create=True) as mock_open:
            mock_open.side_effect = IOError()
            known_violations = read_known_violations("/some/file.json")
        self.assertEqual([], known_violations)
