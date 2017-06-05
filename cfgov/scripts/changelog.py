# -*- coding: utf-8 -*-
"""
This is a script to determine which PRs have been merges since the last
release, or between two releases on the same branch.
"""
import argparse
import re
import os

from collections import namedtuple

import requests

GITHUB_API_URL = 'https://api.github.com'
GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN', None)
GITHUB_HEADERS = {}
if GITHUB_API_TOKEN is not None:
    GITHUB_HEADERS['Authorization'] = 'token ' + GITHUB_API_TOKEN

Commit = namedtuple('Commit', ['sha', 'message'])
PullRequest = namedtuple('PullRequest', ['number', 'title'])


class GitHubError(Exception):
    pass


def get_commit_for_tag(owner, repo, tag):
    """ Get the commit sha for a given git tag """
    tag_url = '/'.join([
        GITHUB_API_URL,
        'repos',
        owner, repo,
        'git', 'refs', 'tags', tag
    ])
    tag_json = {}

    while 'object' not in tag_json or tag_json['object']['type'] != 'commit':
        tag_response = requests.get(tag_url, headers=GITHUB_HEADERS)
        tag_json = tag_response.json()

        if tag_response.status_code != 200:
            raise GitHubError("Unable to get tag {}. {}".format(
                tag, tag_json['message']))

        # If we're given a tag object we have to look up the commit for that tag.
        if tag_json['object']['type'] == 'tag':
            tag_url = tag_json['object']['url']

    return tag_json['object']['sha']


def get_last_commit(owner, repo, branch='master'):
    """ Get the last commit sha for the given repo and branch """
    commits_url = '/'.join([
        GITHUB_API_URL,
        'repos',
        owner, repo,
        'commits'
    ])
    commits_response = requests.get(commits_url, params={'sha': 'master'},
                                    headers=GITHUB_HEADERS)
    commits_json = commits_response.json()
    if commits_response.status_code != 200:
        raise GitHubError("Unable to get commits. {}".format(
            commits_json['message']))

    return commits_json[0]['sha']


def get_commits_between(owner, repo, first_commit, last_commit):
    """ Get a list of commits between two commits """
    commits_url = '/'.join([
        GITHUB_API_URL,
        'repos',
        owner, repo,
        'compare',
        first_commit + '...' + last_commit
    ])
    commits_response = requests.get(commits_url, params={'sha': 'master'},
                                    headers=GITHUB_HEADERS)
    commits_json = commits_response.json()
    if commits_response.status_code != 200:
        raise GitHubError("Unable to get commits between {} and {}. {}".format(
            first_commit, last_commit, commits_json['message']))

    if 'commits' not in commits_json:
        raise GitHubError("Commits not found between {} and {}.".format(
            first_commit, last_commit))

    commits = [Commit(c['sha'], c['commit']['message'])
               for c in commits_json['commits']]
    return commits


def extract_pr(message):
    """ Given a PR merge commit message, extract the PR number and title """
    if 'Merge pull request' not in message:
        raise Exception("Commit isn't a PR merge, {}".format(message))

    # PR merge commits use a double line-break between the branch name
    # and the PR title
    merge, title = message.split('\n\n')

    # Find the PR number
    number_match = re.search(r'#([0-9]+)', merge)
    if number_match is None or len(number_match.groups()) == 0:
        raise Exception("Unable to find PR number in {}".format(merge))
    pr_number = number_match.groups()[0]

    # Output the PR number and title
    return PullRequest(pr_number, title)


def fetch_changes(owner, repo, previous_tag, current_tag=None,
                  branch='master'):
    previous_commit = get_commit_for_tag(owner, repo, previous_tag)

    current_commit = None
    if current_tag is not None:
        current_commit = get_commit_for_tag(owner, repo, current_tag)
    else:
        current_commit = get_last_commit(owner, repo, branch)

    commits_between = get_commits_between(owner, repo,
                                          previous_commit, current_commit)

    # Process the commit list looking for PR merges
    # Look for PR merge commits
    prs = []
    for commit in commits_between:
        if 'Merge pull request' in commit.message:
            prs.append(extract_pr(commit.message))

    if len(prs) == 0 and len(commits_between) > 0:
        raise Exception("Lots of commits and no PRs on branch {}".format(
            branch))

    prs.reverse()
    return prs


def format_changes(owner, repo, prs, markdown=False):
    """ Format the list of prs in either text or markdown """
    lines = []
    for pr in prs:
        number = pr.number
        if markdown:
            link = 'https://github.com/{owner}/{repo}/pull/{number}'.format(
                owner=owner, repo=repo, number=pr.number)
            number = '[#{number}]({link})'.format(number=pr.number, link=link)

        lines.append('- {title} {number}'.format(title=pr.title,
                                                 number=number))

    return lines


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate a CHANGELOG between two git tags based on GitHub"
                    "Pull Request merge commit messages")
    parser.add_argument('owner', metavar='OWNER',
                        help='owner of the repo on GitHub')
    parser.add_argument('repo', metavar='REPO',
                        help='name of the repo on GitHub')
    parser.add_argument('previous_tag', metavar='PREVIOUS',
                        help='previous release tag')
    parser.add_argument('current_tag', metavar='CURRENT', nargs='?',
                        help='current release tag (defaults to HEAD)')
    parser.add_argument('-b', '--branch', default='master',
                        help='branch both releases are tagged from')
    parser.add_argument('-m', '--markdown', action='store_true',
                        help='output in markdown')

    args = parser.parse_args()

    prs = fetch_changes(args.owner, args.repo, args.previous_tag,
                        current_tag=args.current_tag, branch=args.branch)

    for line in format_changes(args.owner, args.repo, prs,
                               markdown=args.markdown):
        print line
