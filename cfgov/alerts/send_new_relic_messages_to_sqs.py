import argparse
import boto3
import logging
import re
import sys

import requests

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
    '--newrelic_url',
    default="https://api.newrelic.com/v2/",
    help='URL base for the New Relic API v2'
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


def get_new_violations(newrelic_token, newrelic_url, threshold, policy_filter):
    """ Check for violations in New Relic that are newer than the
    newness_threshold in minutes. """
    headers = {'X-Api-Key': newrelic_token}
    violations_url = (newrelic_url +
                      'alerts_violations.json?only_open=true')
    r = requests.get(violations_url, headers=headers)
    response_json = r.json()

    violations = []
    for violation in response_json['violations']:
        logger.debug("Found violation: {violation}".format(
                     violation=violation))
        # Filter on the policy name
        policy_name = violation['policy_name']
        if policy_filter.search(policy_name) and \
                violation['duration'] <= threshold:
            violations.append(violation)

    return violations


def format_message_for_violation(violation, account_number):
    """ Format the given violation dictionary into an SQS message
    dictionary """
    title = '{condition_name}, {entity_name}'.format(
        condition_name=violation['condition_name'],
        entity_name=violation['entity']['name']
    )
    incidents_link = (
        'https://alerts.newrelic.com/accounts/'
        '{account_number}/incidents'
    ).format(
        account_number=account_number
    )
    body = (
        'New Relic {product}, {label}.'
        '<a href="{link}">View incidents</a>'
    ).format(
        product=violation['entity']['product'],
        type=violation['entity']['type'],
        label=violation['label'],
        link=incidents_link
    )
    message_body = '{title} - {body}'.format(title=title, body=body)
    return message_body


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

    try:
        policy_filter = re.compile(args.policy_filter)
    except Exception as err:
        logging.error("Unable to compile policy filter regular expression")
        raise err

    violations = get_new_violations(args.newrelic_token,
                                    args.newrelic_url,
                                    args.threshold, policy_filter)
    # Send the violations to SQS as messages
    for violation in violations:
        message_body = format_message_for_violation(
            violation, args.newrelic_account)
        logger.info("Sending message '{}' to SQS".format(message_body))
        if not args.dryrun:
            response = client.send_message(
                QueueUrl=args.queue_url,
                MessageBody=message_body,
            )
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                logger.error("There was an error posting the message "
                             "'{}' to SQS".format(message_body))
                sys.exit(1)
        else:
            logger.info(message_body)
