import boto3
import github3

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Read in messages from specified queue, & post to specified repo'

    def add_arguments(self, parser):
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

    def handle(self, *args, **options):

        # Initialize github API & repo to post to
        gh = github3.login(
            token=options['github_token'],
            url=options['github_url'],
        )
        repo = gh.repository(
            options['github_user'],
            options['github_repo']
        )

        # Initialize Amazon SQS client
        client = boto3.client(
            'sqs',
            aws_access_key_id=options['aws_access_key_id'],
            aws_secret_access_key=options['aws_secret_access_key'],
            region_name='us-east-1',
        )

        # Receive messages from specified SQS queue
        response = client.receive_message(
            QueueUrl=options['queue_url'],
            MaxNumberOfMessages=10,
        )

        # Post these messages to specified Github repo
        for message in response['Messages']:
            body = message['Body']
            repo.create_issue(title=body[:20], body=body)
