import argparse
import boto3
import json
import logging
import github3
import requests

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


def matching_issue(title, issues):
    return next((issue for issue in issues if issue.title == title), None)


def post_to_chat(endpoint, username, message, issue_url):
    text = 'Alert: {}. Github issue at {}'.format(
        message,
        issue_url,
    )
    payload = {
        'text': text,
        'username': args.mattermost_username,
    }
    requests.post(
        args.mattermost_webhook_url,
        data=json.dumps(payload),
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

    # Receive messages from specified SQS queue
    response = client.receive_message(
        QueueUrl=args.queue_url,
        MaxNumberOfMessages=10,
    )

    # Initialize github API & repo to post to
    gh = github3.login(
        token=args.github_token,
        url=args.github_url,
    )
    repo = gh.repository(
        args.github_user,
        args.github_repo,
    )

    for message in response.get('Messages', {}):
        body = message.get('Body')
        title = body.split(" - ")[0]
        logger.info('Retrieved message {} from SQS'.format(body))

        issue = matching_issue(title=title, issues=repo.iter_issues())
        if issue:
            # Issue already exists,
            # add comment to it to document it happened again
            issue.create_comment(body=body)
        else:
            # New issue, post to github
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=[
                    'Maintenance and Response',
                    'alert'
                ],
            )
        # Post to chat, if credentials provided
        if args.mattermost_webhook_url and args.mattermost_username:
            post_to_chat(
                endpoint=args.mattermost_webhook_url,
                username=args.mattermost_username,
                message=body,
                issue_url=issue.html_url,
            )

        client.delete_message(
            QueueUrl=args.queue_url,
            ReceiptHandle=message.get('ReceiptHandle')
        )
        logger.info('Deleted message {} from SQS'.format(body))
