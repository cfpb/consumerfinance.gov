from __future__ import unicode_literals

import argparse
import boto3
import logging

from github_alert import GithubAlert
from mattermost_alert import MattermostAlert

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()

parser.add_argument(
    '--queue_url',
    required=True,
    help='The SQS queue URL to read messages from',
)
parser.add_argument(
    '--aws_access_key_id',
    required=True,
    help='AWS Access Key',
)
parser.add_argument(
    '--aws_secret_access_key',
    required=True,
    help='AWS Secret Access Key',
)
parser.add_argument(
    '--github_token',
    required=True,
    help='Access token for Github account'
)
parser.add_argument(
    '--github_url',
    required=True,
    help='URL for Github (enterprise)'
)
parser.add_argument(
    '--github_user',
    required=True,
    help='Github user that repo lives under'
)
parser.add_argument(
    '--github_repo',
    required=True,
    help='Github repo name to post to'
)
parser.add_argument(
    '--mattermost_webhook_url',
    help='Mattermost webhook URL to post to chatroom'

)
parser.add_argument(
    '--mattermost_username',
    help='Mattermost user that is posting the message'

)


def post_message(body, title, github_creds={}, mattermost_creds={}):
    issue = GithubAlert(github_creds).post(
        title=title,
        body=body,
    )

    if mattermost_creds:
        MattermostAlert(mattermost_creds).post(
            text='Alert: {}. Github issue at {}'.format(
                body,
                issue.html_url,
            )
        )


def cleanup_message(message):
    return message.replace(
        '#', '# '  # Avoids erroneous Github issue link
    ).replace(
        '[Open]', ''  # We want to expand the link
    )


if __name__ == '__main__':
    args = parser.parse_args()

    # Initialize Amazon SQS client
    client = boto3.client(
        'sqs',
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        region_name='us-east-1',
    )

    # Intialize Github credentials
    github_creds = {
        'repo_name': args.github_repo,
        'token': args.github_token,
        'url': args.github_url,
        'user': args.github_user,
    }

    # Initialize Mattermost credentials (optional)
    mattermost_creds = {}
    if args.mattermost_webhook_url and args.mattermost_username:
        mattermost_creds['webhook_url'] = args.mattermost_webhook_url
        mattermost_creds['username'] = args.mattermost_username

    # Receive messages from specified SQS queue
    response = client.receive_message(
        QueueUrl=args.queue_url,
        MaxNumberOfMessages=10,
    )

    for message in response.get('Messages', {}):
        body = cleanup_message(message.get('Body'))
        title = body.split(" - ")[0]

        logger.info('Retrieved message {} from SQS'.format(body))

        post_message(
            body=body,
            title=title,
            github_creds=github_creds,
            mattermost_creds=mattermost_creds,
        )

        client.delete_message(
            QueueUrl=args.queue_url,
            ReceiptHandle=message.get('ReceiptHandle')
        )
        logger.info('Deleted message {} from SQS'.format(body))
