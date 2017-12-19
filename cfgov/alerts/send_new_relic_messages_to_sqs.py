import argparse
import logging
import sys

import boto3

from alerts.newrelic_alerts import NewRelicAlertViolations


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

# add ch to logger
parser = argparse.ArgumentParser()

parser.add_argument(
    '--queue_url',
    required=True,
    help='The SQS queue URL to post messages to',
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
    '--newrelic_token',
    required=True,
    help='Access token for New Relic API'
)
parser.add_argument(
    '--newrelic_account',
    required=True,
    help='New Relic account number, used to construct alert link URLs'
)
parser.add_argument(
    '--known_violations_file',
    required=True,
    help='File to store known New Relic violations across invocations'
)
parser.add_argument(
    '--threshold',
    type=int,
    default=1,
    help='Number of minutes for which to consider a violation "new"'
)
parser.add_argument(
    '--policy_filter',
    default=r'.*',
    help='Filter New Relic violation policy names with the given regex'
)
parser.add_argument(
    '--dryrun',
    action='store_true',
    help='Read from New Relic but do not write to SQS'
)
parser.add_argument(
    '-v', '--verbose',
    action='count',
    default=0,
    help='Increase verbosity, up to three times'
)


def cache_known_violations(known_violations_filename, known_violations):
    with open(known_violations_filename, 'w') as known_violations_file:
        known_violations_file.writelines(
            ["{}\n".format(v) for v in known_violations]
        )

    logger.info("cached known violations {}".format(known_violations))


def read_known_violations(known_violations_filename):
    try:
        with open(known_violations_filename, 'r') as known_violations_file:
            known_violations = [
                int(v) for v in known_violations_file.readlines()
            ]
    except IOError:
        logger.warning("Known violations file does not exist")
        known_violations = []
    logger.info("read known violations {}".format(known_violations))
    return known_violations


def send_violations(sqs_client, queue_url, violation_messages, dryrun=False):
    for message in violation_messages:
        logger.info("Sending message '{}' to SQS".format(message))
        if not dryrun:
            response = sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=message,
            )
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                logger.error("There was an error posting the message "
                             "'{}' to SQS".format(message))
                sys.exit(1)
        else:
            logger.info(message)


if __name__ == "__main__":
    args = parser.parse_args()

    client = boto3.client(
        'sqs',
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        region_name='us-east-1',
    )

    if args.verbose > 0:
        logger.setLevel(logging.DEBUG)

    # Read cached known violations
    known_violations = read_known_violations(args.known_violations_file)

    # Send the violations to SQS as messages
    nralert_violations = NewRelicAlertViolations(
        args.newrelic_token,
        args.policy_filter,
        args.newrelic_account,
        known_violations=known_violations
    )
    messages = nralert_violations.get_new_violation_messages()
    send_violations(client, args.queue_url, messages, dryrun=args.dryrun)

    # Cache known violations
    cache_known_violations(args.known_violations_file,
                           nralert_violations.known_violations)
