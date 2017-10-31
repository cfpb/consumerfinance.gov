from unittest import TestCase


class TestResolveGitHubIssues(TestCase):
    def test_import_works(self):
        """This script is difficult to test, but we can test module import.

        That way if in future someone removes the github3 dependency, this
        test will fail.
        """
        from scripts import resolve_github_issues  # flake8: noqa
