import json
import os
from unittest.mock import patch

from django.test import TestCase

from github3.issues.issue import ShortIssue
from github3.repos.repo import ShortRepository
from github3.session import GitHubSession

from alerts.github_alert import GithubAlert


JSON_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/json"


class TestGithubAlert(TestCase):
    session = GitHubSession()
    session.basic_auth("test", "test")

    with open(f"{JSON_DIR}/github_repository.json") as f:
        repository = ShortRepository(json.load(f), session)

    with open(f"{JSON_DIR}/github_closed_issue.json") as f:
        closed_issue = ShortIssue(json.load(f), session)

    with open(f"{JSON_DIR}/github_open_issue.json") as f:
        open_issue = ShortIssue(json.load(f), session)

    def setUp(self):
        self.text = "foö"

    @patch("github3.issues.issue._Issue.create_comment")
    @patch(
        "alerts.github_alert.GithubAlert.matching_issue",
        return_value=open_issue,
    )
    def test_comment(self, matching_issue, create_comment):
        """Test that we add a comment when a matching issue is found"""
        GithubAlert({}).post(title=self.text, body=self.text)
        create_comment.assert_called_once_with(body=self.text)

    @patch("github3.issues.issue._Issue.create_comment")
    @patch("github3.issues.issue._Issue.reopen")
    @patch(
        "alerts.github_alert.GithubAlert.matching_issue",
        return_value=closed_issue,
    )
    def test_reopen(self, matching_issue, reopen, create_comment):
        """Test that we reopen a Github issue if it was previously closed"""
        GithubAlert({}).post(title=self.text, body=self.text)
        reopen.assert_called_once_with()

    @patch("github3.repos.repo._Repository.create_issue")
    @patch(
        "alerts.github_alert.GithubAlert.repo",
        return_value=repository,
    )
    @patch(
        "alerts.github_alert.GithubAlert.matching_issue",
        return_value=None,
    )
    def test_create_issue(self, matching_issue, repo, create_issue):
        """Test that we create an issue when no issue is found"""
        GithubAlert({}).post(title=self.text, body=self.text)
        create_issue.assert_called_once_with(
            title=self.text,
            body=self.text,
            labels=["alert"],
        )
