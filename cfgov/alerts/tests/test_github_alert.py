# -*- coding: utf-8 -*-
from unittest.mock import patch

from django.test import TestCase

import github3

from alerts.github_alert import GithubAlert


class TestGithubAlert(TestCase):

    closed_issue = github3.issues.issue.Issue(
        {
            'html_url': 'https://github.com/foo/bar/issues/1',
            'labels': [],
            'user': {},
            'closed_at': '2017-02-12T13:22:01Z',
        }
    )

    open_issue = github3.issues.issue.Issue(
        {
            'html_url': 'https://github.com/foo/bar/issues/2',
            'labels': [],
            'user': {},
            'closed_at': None,
        }
    )

    def setUp(self):
        self.text = u'foö'

    @patch('github3.issues.issue.Issue.create_comment')
    @patch(
        'alerts.github_alert.GithubAlert.matching_issue',
        return_value=open_issue
    )
    def test_comment(self, matching_issue, create_comment):
        """ Test that we add a comment when a matching issue is found """
        GithubAlert({}).post(title=self.text, body=self.text)
        create_comment.assert_called_once_with(body=self.text)

    @patch('github3.issues.issue.Issue.create_comment')
    @patch('github3.issues.issue.Issue.reopen')
    @patch(
        'alerts.github_alert.GithubAlert.matching_issue',
        return_value=closed_issue
    )
    def test_reopen(self, matching_issue, reopen, create_comment):
        """ Test that we reopen a Github issue if it was previously closed """
        GithubAlert({}).post(title=self.text, body=self.text)
        reopen.assert_called_once_with()

    @patch('github3.repos.repo.Repository.create_issue')
    @patch(
        'alerts.github_alert.GithubAlert.repo',
        return_value=github3.repos.repo.Repository({})
    )
    @patch(
        'alerts.github_alert.GithubAlert.matching_issue',
        return_value=None,
    )
    def test_create_issue(self, matching_issue, repo, create_issue):
        """ Test that we create an issue when no issue is found """
        GithubAlert({}).post(title=self.text, body=self.text)
        create_issue.assert_called_once_with(
            title=self.text,
            body=self.text,
            labels=[
                'alert'
            ],
        )
