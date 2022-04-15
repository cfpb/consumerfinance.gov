import unittest
from unittest import mock

from django.core.management import call_command


class CommandTests(unittest.TestCase):
    def setUp(self):
        stdout_patch = mock.patch("sys.stdout")
        stdout_patch.start()
        self.addCleanup(stdout_patch.stop)

    @mock.patch(
        "paying_for_college.management.commands."
        "tag_schools.tag_settlement_schools.tag_schools"
    )
    def test_tag_schools(self, mock_tag):
        mock_tag.return_value = "Aye Aye"
        call_command("tag_schools", "s3URL")
        self.assertEqual(mock_tag.call_count, 1)

    @mock.patch("paying_for_college.management.commands.purge.purge")
    def test_purges(self, mock_purge):
        mock_purge.return_value = "Aye Aye"
        call_command("purge", "notifications")
        self.assertEqual(mock_purge.call_count, 1)
        call_command("purge", "programs")
        self.assertEqual(mock_purge.call_count, 2)
        call_command("purge", "")
        self.assertEqual(mock_purge.call_count, 3)
        call_command("purge", "schools")
        self.assertEqual(mock_purge.call_count, 4)

    @mock.patch(
        "paying_for_college.management.commands.update_ipeds.load_values"
    )
    def test_update_ipeds(self, mock_load):
        mock_load.return_value = "DRY RUN"
        call_command("update_ipeds")
        self.assertEqual(mock_load.call_count, 1)
        call_command("update_ipeds", "--dry-run", "false")
        self.assertEqual(mock_load.call_count, 2)
        call_command("update_ipeds", "--dry-run", "jabberwocky")
        self.assertEqual(mock_load.call_count, 2)

    @mock.patch(
        "paying_for_college.management.commands."
        "update_via_api.update_colleges.update"
    )
    def test_api_command_calls_update(self, mock_update):
        mock_update.return_value = ([], "OK")
        call_command("update_via_api")
        self.assertTrue(mock_update.call_count == 1)
        call_command("update_via_api", "--school_id", "999999")
        self.assertTrue(mock_update.call_count == 2)
        self.assertTrue(mock_update.called_with(single_school=999999))
        call_command(
            "update_via_api", "--school_id", "999999", "--save_programs"
        )
        self.assertTrue(mock_update.call_count == 3)
        self.assertTrue(
            mock_update.called_with(single_school=999999, store_programs=True)
        )
        call_command("update_via_api", "--save_programs")
        self.assertTrue(mock_update.call_count == 4)
        self.assertTrue(mock_update.called_with(store_programs=True))

    @mock.patch(
        "paying_for_college.management.commands."
        "load_programs.load_programs.load"
    )
    def test_load_programs(self, mock_load):
        mock_load.return_value = ([], "OK")
        call_command("load_programs", "filename")
        self.assertEqual(mock_load.call_count, 1)
        mock_load.assert_called_once_with("filename")
        mock_load.return_value = (["failure"], "not OK")
        call_command("load_programs", "filename")
        self.assertEqual(mock_load.call_count, 2)
        call_command("load_programs", "filename", "--s3", "true")
        self.assertEqual(mock_load.call_count, 3)
        mock_error = mock.Mock()
        mock_error.side_effect = Exception("Mock Error!")
        mock_load.return_value = mock_error
        error_state = call_command("load_programs", "filename")
        self.assertTrue(error_state is None)

    @mock.patch(
        "paying_for_college.management.commands."
        "load_programs.load_programs.load"
    )
    def test_load_programs_more_than_1_files(self, mock_load):
        mock_load.return_value = ([], "OK")
        call_command("load_programs", "filename", "filename2", "filename3")
        self.assertEqual(mock_load.call_count, 3)
        mock_load.assert_has_calls(
            [
                mock.call("filename"),
                mock.call("filename2"),
                mock.call("filename3"),
            ]
        )

    @mock.patch(
        "paying_for_college.management.commands."
        "retry_notifications.retry_notifications"
    )
    def test_retry_notifications(self, mock_retry):
        mock_retry.return_value = "notified"
        call_command("retry_notifications")
        self.assertEqual(mock_retry.call_count, 1)
        call_command("retry_notifications", "--days", "2")
        self.assertEqual(mock_retry.call_count, 2)
        self.assertTrue(mock_retry.called_with(days=2))

    @mock.patch(
        "paying_for_college.management.commands."
        "send_stale_notifications.send_stale_notifications"
    )
    def test_send_stale_notifications(self, mock_send):
        mock_send.return_value = "notified"
        call_command("send_stale_notifications")
        self.assertEqual(mock_send.call_count, 1)
        call_command(
            "send_stale_notifications", "--add-email", "fake@fake.com"
        )
        self.assertEqual(mock_send.call_count, 2)
        self.assertTrue(mock_send.called_with(add_email=["fake@fake.com"]))
