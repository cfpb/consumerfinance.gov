import os

import github3
from github3.issues.issue import ShortIssue
from github3.repos.repo import Repository


class GithubAlert:
    def __init__(self, credentials):
        self.token = credentials.get("token", os.environ.get("GITHUB_TOKEN"))
        self.url = credentials.get("url", os.environ.get("GITHUB_URL"))
        self.user = credentials.get("user", os.environ.get("GITHUB_USER"))
        self.repo_name = credentials.get(
            "repo_name", os.environ.get("GITHUB_REPO")
        )

    def repo(self) -> Repository:
        gh = github3.enterprise_login(  # pragma: no cover
            token=self.token,
            url=self.url,
        )
        return gh.repository(self.user, self.repo_name)

    def matching_issue(self, title) -> ShortIssue:
        issues = self.repo().issues(state="all")  # pragma: no cover
        return next((issue for issue in issues if issue.title == title), None)

    def post(self, title, body, labels=None) -> ShortIssue:
        if not labels:
            labels = ["alert"]
        # Truncate the title if needed, max is 256 chars
        title = title[:256]
        issue = self.matching_issue(title)
        if issue:  # Issue already exists
            if issue.is_closed():
                issue.reopen()
            # add comment to it to document it happened again
            issue.create_comment(body=body)
        else:
            # New issue, post to github
            issue = self.repo().create_issue(
                title=title,
                body=body,
                labels=labels,
            )
        return issue
