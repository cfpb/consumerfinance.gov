# -*- coding: utf-8 -*-

from unittest import TestCase

import mock

from scripts.changelog import (
    GitHubError,
    get_commit_for_tag,
    get_last_commit,
    get_commits_between,
    extract_pr,
)



class TestChangelog(TestCase):

    def setUp(self):
        pass

    @mock.patch('requests.get')
    def test_get_commit_for_tag_exists(self, mock_requests_get):
        """ Test getting the commit sha for a tag if the tag exists """
        response = mock.MagicMock()
        response.status_code = 200
        response.json.return_value = {'object': { 'sha': '0123456789abcdef' }}
        mock_requests_get.return_value = response
        result = get_commit_for_tag('someone', 'one-repo', 'myorg')
        self.assertEqual(result, '0123456789abcdef')

    @mock.patch('requests.get')
    def test_get_commit_for_tag_not_found(self, mock_requests_get):
        """ Test getting the commit sha for a tag if the tag exists """
        response = mock.MagicMock()
        response.status_code = 404
        response.json.return_value = {'message': 'nope'}
        mock_requests_get.return_value = response
        with self.assertRaises(GitHubError):
            get_commit_for_tag('someone', 'one-repo', 'myorg')

    @mock.patch('requests.get')
    def test_get_last_commit_exists(self, mock_requests_get):
        """ Test getting the commit sha for a tag if the tag exists """
        response = mock.MagicMock()
        response.status_code = 200
        response.json.return_value = [{ 'sha': '0123456789abcdef' }]
        mock_requests_get.return_value = response
        result = get_last_commit('someone', 'one-repo')
        self.assertEqual(result, '0123456789abcdef')

    @mock.patch('requests.get')
    def test_get_last_commit_not_found(self, mock_requests_get):
        """ Test getting the commit sha for a tag if the tag exists """
        response = mock.MagicMock()
        response.status_code = 404
        response.json.return_value = {'message': 'nope'}
        mock_requests_get.return_value = response
        with self.assertRaises(GitHubError):
            get_last_commit('someone', 'one-repo')

    @mock.patch('requests.get')
    def test_get_commits_between(self, mock_requests_get):
        """ Test getting commits between two commits """
        response = mock.MagicMock()
        response.status_code = 200
        response.json.return_value = {
            'commits': [
                {
                    'sha': '0123456789abcdef',
                    'commit': {'message': 'Foo'},
                },
                {
                    'sha': '123456789abcdef0',
                    'commit': {'message': 'Bar'},
                },
            ]
        }
        mock_requests_get.return_value = response
        result = get_commits_between('someone', 'one-repo', 'one', 'two')
        self.assertEqual(
            result, [('0123456789abcdef', 'Foo'), ('123456789abcdef0', 'Bar')])

    @mock.patch('requests.get')
    def test_get_commits_between_no_commits(self, mock_requests_get):
        """ Test when there are no commits in the data """
        response = mock.MagicMock()
        response.status_code = 200
        response.json.return_value = {}
        mock_requests_get.return_value = response
        with self.assertRaises(GitHubError):
            get_commits_between('someone', 'one-repo', 'one', 'two')

    @mock.patch('requests.get')
    def test_get_commits_between_not_found(self, mock_requests_get):
        """ Test when one commit is not found """
        response = mock.MagicMock()
        response.status_code = 404
        response.json.return_value = {'message': 'nope'}
        mock_requests_get.return_value = response
        with self.assertRaises(GitHubError):
            get_commits_between('someone', 'one-repo', 'one', 'two')

    def test_extract_pr(self):
        """ Test our PR formatter """
        message = 'Merge pull request #1234 from some/branch\n\nMy Title'
        result = extract_pr(message)
        self.assertEqual(result.number, '1234')
        self.assertEqual(result.title, 'My Title')

    def test_extract_pr_not_pr(self):
        """ Test our PR formatter with non-PR message """
        message = 'I made some changes!'
        with self.assertRaises(Exception):
            extract_pr(message)

    def test_extract_pr_no_number(self):
        """ Test our PR formatter with non-PR message """
        message = 'Merge pull request from some/branch\n\nMy Title'
        with self.assertRaises(Exception):
            extract_pr(message)
