import argparse
import boto3
import logging
import github3

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


if __name__ == '__main__':
    args = parser.parse_args()
    # Initialize github API & repo to post to
    gh = github3.login(
        token=args.github_token,
        url=args.github_url,
    )
    repo = gh.repository(
        args.github_user,
        args.github_repo,
    )

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

    if 'Messages' in response:
        # Post these messages to specified Github repo
        for message in response['Messages']:
            body = message['Body']
            logger.info('Retrieved message {} from SQS'.format(body))
            repo.create_issue(title=body[:20], body=body)
