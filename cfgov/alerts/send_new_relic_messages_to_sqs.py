import argparse
import logging
import sys

from alerts.newrelic_alerts import NewRelicAlertViolations
from alerts.sqs_queue import SQSQueue

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

# add ch to logger
parser = argparse.ArgumentParser()

parser.add_argument(
    "--queue_url",
    required=True,
    help="The SQS queue URL to post messages to",
)
parser.add_argument(
    "--aws_access_key_id",
    required=True,
    help="AWS Access Key",
)
parser.add_argument(
    "--aws_secret_access_key",
    required=True,
    help="AWS Secret Access Key",
)
parser.add_argument(
    "--newrelic_token", required=True, help="Access token for New Relic API"
)
parser.add_argument(
    "--newrelic_account",
    required=True,
    help="New Relic account number, used to construct alert link URLs",
)
parser.add_argument(
    "--known_violations_file",
    required=True,
    help="File to store known New Relic violations across invocations",
)
parser.add_argument(
    "--threshold",
    type=int,
    default=1,
    help='Number of minutes for which to consider a violation "new"',
)
parser.add_argument(
    "--policy_filter",
    default=r".*",
    help="Filter New Relic violation policy names with the given regex",
)
parser.add_argument(
    "--dryrun",
    action="store_true",
    help="Read from New Relic but do not write to SQS",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Increase verbosity, up to three times",
)


def cache_known_violations(known_violations_filename, known_violations):
    with open(known_violations_filename, "w") as known_violations_file:
        known_violations_file.writelines(
            ["{}\n".format(v) for v in known_violations]
        )

    logger.info("cached known violations {}".format(known_violations))


def read_known_violations(known_violations_filename):
    try:
        with open(known_violations_filename, "r") as known_violations_file:
            known_violations = [
                int(v) for v in known_violations_file.readlines()
            ]
    except IOError:
        logger.warning("Known violations file does not exist")
        known_violations = []
    logger.info("read known violations {}".format(known_violations))
    return known_violations


if __name__ == "__main__":
    args = parser.parse_args()

    if args.verbose > 0:
        logger.setLevel(logging.DEBUG)

    # Read cached known violations
    known_violations = read_known_violations(args.known_violations_file)

    # Send the violations to SQS as messages
    nralert_violations = NewRelicAlertViolations(
        args.newrelic_token,
        args.policy_filter,
        args.newrelic_account,
        known_violations=known_violations,
    )

    sqs_queue = SQSQueue(
        queue_url=args.queue_url,
        credentials={
            "access_key": args.aws_access_key_id,
            "secret_key": args.aws_secret_access_key,
        },
    )

    for message in nralert_violations.get_new_violation_messages():
        if args.dryrun:
            logger.info(message)
            continue
        response = sqs_queue.post(message)
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            sys.exit(1)
        logger.info("Sent message '{}' to SQS".format(message))

    # Cache known violations
    cache_known_violations(
        args.known_violations_file, nralert_violations.known_violations
    )
