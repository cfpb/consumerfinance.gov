import argparse
import logging
# import subprocess
import sys
import time

import requests


logger = logging.getLogger('http_smoke_tests')
logger.setLevel(logging.FATAL)
shell_log = logging.StreamHandler()
shell_log.setLevel(logging.INFO)
logger.addHandler(shell_log)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--base",
    help="choose a server base other than www.consumerfinance.gov"
)
parser.add_argument(
    "--full",
    action="store_true",
    help=("If --full is used, the script will check all urls in our main nav, "
          "plus a selection of our most-visited pages.")
)
parser.add_argument(
    "-v", "--verbose",
    action="store_true",
    help="Set logging level to info to see all message output."
)
parser.add_argument(
    "-t", "--timeout",
    type=str,
    help="Set a timeout level, in seconds; the default is 30."
)

TIMEOUT = 30
ALLOWED_TIMEOUTS = 1
FULL = False
BASE = 'https://www.consumerfinance.gov'
S3_URI = 'http://files.consumerfinance.gov.s3.amazonaws.com/build/smoketests/smoketest_urls.json'  # noqa

# These are URL's that exist in a fresh copy of the site
# after migrations and initial_data are run
SHORT_RUN = [
    '/',
    '/your-story/',
    '/find-a-housing-counselor/',
    '/know-before-you-owe/',
    '/fair-lending/',
    '/data-research/consumer-complaints/',
]

# Fall-back top-20 URLs, as of July 2019, from hubcap/wiki
TOP20 = [
    '/',  # home page
    '/find-a-housing-counselor/',
    '/learnmore/',
    '/complaint/',
    '/ask-cfpb/what-is-the-best-way-to-negotiate-a-settlement-with-a-debt-collector-en-1447/',  # noqa
    '/complaint/getting-started/',
    '/policy-compliance/rulemaking/regulations/',
    '/policy-compliance/rulemaking/regulations/1026/',
    '/policy-compliance/guidance/tila-respa-disclosure-rule/',
    '/ask-cfpb/what-is-a-debt-to-income-ratio-why-is-the-43-debt-to-income-ratio-important-en-1791/',  # noqa
    '/data-research/consumer-complaints/',
    '/policy-compliance/guidance/',
    '/ask-cfpb/how-do-i-stop-automatic-payments-from-my-bank-account-en-2023/',
    '/ask-cfpb/what-should-i-do-when-a-debt-collector-contacts-me-en-1695/',
    '/ask-cfpb/how-do-i-get-a-copy-of-my-credit-reports-en-5/',
    '/ask-cfpb/',
    '/data-research/consumer-complaints/search/',
    '/about-us/contact-us/',
    '/about-us/the-bureau/',
    '/owning-a-home/',
]

# Fall-back URLs for cfgov sub-apps that are expected to be present
APPS = [
    '/es/',
    '/es/obtener-respuestas/',
    '/students/',
    '/servicemembers/',
    '/know-before-you-owe/',
    '/fair-lending/',
    '/paying-for-college/',
    '/paying-for-college2/understanding-your-financial-aid-offer/about-this-tool/',  # noqa
    '/retirement/before-you-claim/',
    '/retirement/before-you-claim/es/',
    '/consumer-tools/auto-loans/',
    '/consumer-tools/credit-reports-and-scores/',
    '/consumer-tools/debt-collection/',
    '/consumer-tools/prepaid-cards/',
    '/mortgagehelp/',
    '/sending-money/',
    '/practitioner-resources/your-money-your-goals/',
    '/adult-financial-education/',
    '/practitioner-resources/youth-financial-education/',
    '/practitioner-resources/library-resources/',
    '/practitioner-resources/resources-for-tax-preparers/',
    '/consumer-tools/money-as-you-grow/',
    '/empowerment/',
    '/practitioner-resources/resources-for-older-adults/',
    '/data-research/',
    '/data-research/research-reports/',
    '/data-research/cfpb-research-conference/',
    '/data-research/consumer-complaints/',
    '/data-research/hmda/',
    '/data-research/hmda/for-filers',
    '/data-research/consumer-credit-trends/',
    '/data-research/credit-card-data/',
    '/data-research/cfpb-researchers/',
    '/data-research/mortgage-performance-trends/',
    '/policy-compliance/',
    '/policy-compliance/rulemaking/',
    '/policy-compliance/guidance/',
    '/policy-compliance/guidance/implementation-guidance/',
    '/policy-compliance/enforcement/',
    '/policy-compliance/notice-opportunities-comment/',
    '/policy-compliance/amicus/',
    '/policy-compliance/guidance/implementation-guidance/hmda-implementation/',
    '/policy-compliance/guidance/implementation-guidance/mortserv/',
    '/policy-compliance/guidance/implementation-guidance/tila-respa-disclosure-rule/',  # noqa: E501
    '/about-us/budget-strategy/',
    '/about-us/payments-harmed-consumers/',
    '/about-us/blog/',
    '/about-us/newsroom/',
    '/about-us/events/',
    '/about-us/careers/',
    '/about-us/careers/current-openings/',
    '/about-us/doing-business-with-us/',
    '/about-us/innovation/',
    '/activity-log/',
    '/your-story/',
]

FULL_RUN = sorted(set(TOP20 + APPS))


def get_full_list():
    try:
        url_data = requests.get(S3_URI).json()
    except Exception as e:
        logger.info(
            'Using fallback because request for S3 list failed: {}'.format(e))
        full_run = FULL_RUN
    else:
        print("URLs acquired from S3")
        full_run = sorted(set(url_data.get('top20') + url_data.get('apps')))
    return full_run


def check_urls(base, full=False):
    """
    A smoke test to make sure the main cfgov URLs are returning status 200.

    The full option tests megamenu links, plus the 20 most-popular pages.
    """
    count = 0
    timeouts = []
    failures = []
    starter = time.time()
    if full:
        url_list = get_full_list()
    else:
        url_list = SHORT_RUN
    for url_suffix in url_list:
        logger.info(url_suffix)
        count += 1
        url = '{}{}'.format(base, url_suffix)
        try:
            response = requests.get(url, timeout=TIMEOUT)
            code = response.status_code
            if code == 200:
                pass
            else:
                logger.info("{} failed with status code "
                            "'{}'".format(url, code))
                failures.append((url, code))
        except requests.exceptions.Timeout:
            logger.info('{} timed out'.format(url))
            timeouts.append(url)
        except requests.exceptions.ConnectionError as e:
            logger.info("{} returned a connection error".format(url))
            failures.append((url, e))
        except requests.exceptions.RequestException as e:
            logger.info("{} failed for '{}'".format(url, e))
            failures.append((url, e))
    timer = int(time.time() - starter)
    logger.info(
        "\n{} took {} seconds to check {} URLs at {}\n  "
        "{} failed\n  "
        "{} timed out".format(
            sys.argv[0],
            timer,
            count,
            base,
            len(failures),
            len(timeouts)
        )
    )

    if failures:
        logger.error("These URLs failed: {}".format(failures))
    if len(timeouts) > ALLOWED_TIMEOUTS:
        logger.error("These URLs timed out after {} seconds: "
                     "{}".format(TIMEOUT, timeouts))
    elif timeouts:
        logger.info(
            "{} allowed timeouts occurred:\n"
            "{}".format(len(timeouts), "\n".join(timeouts)))

    if failures or len(timeouts) > ALLOWED_TIMEOUTS:
        logger.error("FAIL")
        return False

    logger.info("\x1B[32mAll URLs return 200. No smoke!\x1B[0m")
    return True


if __name__ == '__main__':  # pragma: nocover
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
    if args.base:
        BASE = args.base
    if args.full:
        FULL = True
    if args.timeout:
        TIMEOUT = int(args.timeout)
    if not check_urls(BASE, full=FULL):
        sys.exit(1)
