#!/usr/bin/env python
import argparse
import logging
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
    "--url_list",
    type=str,
    nargs='+',
    help=("You can provide a space-separated custom list "
          "of relative URLs to check.")
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

# Fall-back list of top 25 URLs, as of Jan.2, 2020, from hubcap/wiki
TOP = [
    '/',  # home page
    '/learnmore/',
    '/complaint/',
    '/find-a-housing-counselor/',
    '/ask-cfpb/what-is-the-best-way-to-negotiate-a-settlement-with-a-debt-collector-en-1447/',  # noqa
    '/ask-cfpb/what-should-i-do-when-a-debt-collector-contacts-me-en-1695/',
    '/complaint/getting-started/',
    '/ask-cfpb/what-is-a-debt-to-income-ratio-why-is-the-43-debt-to-income-ratio-important-en-1791/',  # noqa
    '/policy-compliance/rulemaking/regulations/',
    '/consumer-tools/debt-collection/',
    '/policy-compliance/guidance/tila-respa-disclosure-rule/',
    '/ask-cfpb/how-do-i-stop-automatic-payments-from-my-bank-account-en-2023/',
    '/policy-compliance/rulemaking/regulations/1026/',
    '/data-research/consumer-complaints',
    '/data-research/consumer-complaints/search/?from=0&searchfield=all&searchtext=&size=25&sort=created_date_desc',  # noqa
    '/policy-compliance/guidance/',
    '/consumer-tools/prepaid-cards/',
    '/ask-cfpb/how-do-i-get-a-copy-of-my-credit-reports-en-5/',
    '/about-us/contact-us/',
    '/ask-cfpb/',
    '/complaint/process/',
    '/about-us/careers/current-openings/',
    '/about-us/the-bureau/',
    '/consumer-tools/credit-reports-and-scores/',
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

# call `set` on the combined list to weed out dupes
FULL_RUN = sorted(set(TOP + APPS))


def get_full_list():
    """Fetch a list of URLs to test from s3, or fall back to local default."""
    try:
        url_data = requests.get(S3_URI).json()
    except Exception as e:
        logger.warning(
            'Using fallback because request for S3 list failed: {}'.format(e))
        full_run = FULL_RUN
    else:
        full_run = sorted(set(url_data.get('top') + url_data.get('apps')))
    return full_run


def check_urls(base, url_list=None):
    """
    A smoke test to make sure the main cfgov URLs are returning status 200.

    Providing no `url_list` will test a standard list of important site URLs,
    which includes megamenu links, main apps, and our 25 most popular pages.

    Passing no base value will run the tests against production.

    To run the full suite against production, and see its progress:

    ./cfgov/scripts/http_smoke_test.py -v

    You can test a custom set of URLs by passing relative URL strings
    (relative to the provided base) as the `url_list` value. 
    This example tests two URLs against a local cfgov instance:

    ./cfgov/scripts/http_smoke_test.py -v --base 'http://localhost:8000' --url_list '/' '/retirement/before-you-claim/'  # noqa
    """
    count = 0
    timeouts = []
    failures = []
    starter = time.time()
    if not url_list:
        url_list = get_full_list()
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
    url_list = None
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
    if args.base:
        BASE = args.base
    if args.url_list:
        url_list = args.url_list
    if args.timeout:
        TIMEOUT = int(args.timeout)
    if not check_urls(BASE, url_list=url_list):
        sys.exit(1)
