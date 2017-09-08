import os

import github3


class GithubAlert:
    def __init__(self, credentials):
        token = credentials.get(
            'token',
            os.environ.get('GITHUB_TOKEN')
        )
        url = credentials.get(
            'url',
            os.environ.get('GITHUB_URL')
        )
        user = credentials.get(
            'user',
            os.environ.get('GITHUB_USER')
        )
        repo_name = credentials.get(
            'repo_name',
            os.environ.get('GITHUB_REPO')
        )

        gh = github3.login(
            token=token,
            url=url,
        )

        self.repo = gh.repository(user, repo_name)

    def matching_issue(self, title):
        issues = self.repo.iter_issues(state='all')
        return next((issue for issue in issues if issue.title == title), None)

    def post(self, title, body):
        issue = self.matching_issue(title)
        if issue:  # Issue already exists
            if issue.is_closed():
                issue.reopen()
            # add comment to it to document it happened again
            issue.create_comment(body=body)
        else:
            # New issue, post to github
            issue = self.repo.create_issue(
                title=title,
                body=body,
                labels=[
                    'Maintenance and Response',
                    'alert'
                ],
            )
        return issue
