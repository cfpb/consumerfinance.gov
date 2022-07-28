# -*- coding: utf-8 -*-
from unittest.mock import patch

from django.test import TestCase

import github3

from alerts.github_alert import GithubAlert
from alerts.mattermost_alert import MattermostAlert
from alerts.post_sqs_messages import process_sqs_message


class TestPostSQSMessages(TestCase):

    issue = github3.issues.issue.Issue(
        {
            "html_url": "https://github.com/foo/bar/issues/42",
            "labels": [],
            "user": {},
        }
    )

    @patch("alerts.mattermost_alert.MattermostAlert.post")
    @patch("alerts.github_alert.GithubAlert.post", return_value=issue)
    def test_process_sqs_message(self, github_post, mattermost_post):
        """Test that we post to Github and
        Mattermost with the desired information
        """
        process_sqs_message(
            {"Body": "Test Job #1234 - Failed"},
            GithubAlert({}),
            MattermostAlert({}),
        )

        github_post.assert_called_once_with(
            title="Test Job # 1234", body="Test Job # 1234 - Failed"
        )
        mattermost_post.assert_called_once_with(
            text=(
                "Alert: Test Job # 1234. "
                "Github issue at https://github.com/foo/bar/issues/42"
            )
        )

    @patch(
        "alerts.mattermost_alert.MattermostAlert.post", side_effect=Exception
    )
    @patch("alerts.github_alert.GithubAlert.post")
    def test_mattermost_failure_ignored(self, gh, mm):
        process_sqs_message(
            {"Body": "Test Job #1234 - Failed"},
            GithubAlert({}),
            MattermostAlert({}),
        )
