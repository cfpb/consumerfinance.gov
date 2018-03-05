#!/usr/bin/env python
"""
This script can be used to test and close GitHub issues that were opened in
response to a failing (500) HTTP status code.

Invoke it like:

    $ ./resolve_github_issues.py \
        --token your-github-api-token \
        --url base-github-url \
        --owner issue-repository-owner \
        --repository issue-repository-name \
        --url-base test-url-base \
        --close-comment "Closing this issue because fixed." \
        --title-regex "/foo/bar/baz"

This accesses the GitHub API at base-github-url, using the API token provided
by your-github-api-token. It looks at the repository named
issue-repository-owner/issue-repository-name, at all issues whose title
includes the regex "/foo/bar/baz".

Issues are assumed to be titled something like

    "Internal Server Error: /some/path"

where the title ends with a relative URL path that triggered a 500 error. This
relative path is combined with the url-base argument to create an absolute URL
that can be used to verify if the link is still broken.

If not (if it returns a 200 status code), then the issue can be automatically
closed if a comment is passed to the close-comment argument.
"""
from __future__ import print_function, unicode_literals

import argparse
import github3
import re
import requests


url_regex = re.compile(' (/[^ ]*)$')


def run(token, url, owner, repository, url_base, close_comment=None,
        title_regex=None):
    gh = github3.login(token=token, url=url)
    repo = gh.repository(owner=owner, repository=repository)

    if title_regex:
        title_regex = re.compile(title_regex)

    for issue in repo.iter_issues(state='open', labels='alert'):
        if title_regex:
            if not title_regex.search(issue.title):
                continue

        url_match = url_regex.search(issue.title)

        if not url_match:
            continue

        url = url_base + url_match.group(1)

        print(issue.number, 'testing URL:', url)
        response = requests.get(url)

        if response.status_code != 200:
            print('FAILED', response.status_code)
            continue

        if close_comment:
            print('closing issue', issue.number)
            issue.create_comment(close_comment)
            issue.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='GitHub API token', required=True)
    parser.add_argument('--url', help='GitHub base URL', required=True)
    parser.add_argument('--owner', help='GitHub repository owner',
                        required=True)
    parser.add_argument('--repository', help='GitHub repository name',
                        required=True)
    parser.add_argument('--url-base',
                        default='https://www.consumerfinance.gov',
                        help='base URL, defaults to %(default)s')
    parser.add_argument('--close-comment',
                        help='close issues with this comment (optional)')
    parser.add_argument('--title-regex',
                        help=(
                            'only test issues whose title matches '
                            'this regular expression'
                        ))
    run(**vars(parser.parse_args()))
