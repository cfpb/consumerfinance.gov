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
S3_URI = 'https://files.consumerfinance.gov/build/smoketests/smoketest_urls.json'  # noqa: E501

# Fall-back list of top 20 URLs, as of April 2, 2021, from hubcap/wiki
# All URLs in the list should be canonical locations of the given pages,
# not redirects.
TOP = [
    '/',  # home page
    '/about-us/blog/guide-covid-19-economic-stimulus-checks/',
    '/coronavirus/mortgage-and-housing-assistance/mortgage-relief/',
    '/find-a-housing-counselor/',
    '/complaint/',
    '/learnmore/',
    '/ask-cfpb/what-is-the-best-way-to-negotiate-a-settlement-with-a-debt-collector-en-1447/',  # noqa: E501
    '/coronavirus/mortgage-and-housing-assistance/renter-protections/',
    '/about-us/blog/cares-act-early-retirement-withdrawal/',
    '/about-us/blog/claim-economic-impact-payments-for-new-dependents/',
    '/consumer-tools/prepaid-cards/',
    '/about-us/blog/economic-impact-payment-prepaid-card/',
    '/complaint/getting-started/',
    '/coronavirus/mortgage-and-housing-assistance/',
    '/ask-cfpb/what-is-the-difference-between-a-mortgage-interest-rate-and-an-apr-en-135/',
    '/ask-cfpb/what-should-i-do-when-a-debt-collector-contacts-me-en-1695/',
    '/about-us/contact-us/',
    '/coronavirus/managing-your-finances/economic-impact-payment-prepaid-debit-cards/',  # noqa: E501
    '/rules-policy/regulations/',
    '/ask-cfpb/what-is-a-debt-to-income-ratio-why-is-the-43-debt-to-income-ratio-important-en-1791/',  # noqa: E501
]

# URLs for cfgov sub-apps that are expected to be present
# All URLs in the list should be canonical locations of the given pages,
# not redirects.
APPS = [
    '/about-us/budget-strategy/',
    '/enforcement/payments-harmed-consumers/',
    '/about-us/blog/',
    '/about-us/newsroom/',
    '/about-us/events/',
    '/about-us/careers/',
    '/about-us/careers/current-openings/',
    '/about-us/doing-business-with-us/',
    '/rules-policy/innovation/',
    '/activity-log/',
    '/ask-cfpb/',
    '/your-story/',
    '/es/',
    '/es/obtener-respuestas/',
    '/students/',
    '/consumer-tools/educator-tools/servicemembers/',
    '/know-before-you-owe/',
    '/fair-lending/',
    '/paying-for-college/',
    '/paying-for-college2/understanding-your-financial-aid-offer/about-this-tool/',  # noqa: E501
    '/retirement/before-you-claim/',
    '/retirement/before-you-claim/es/',
    '/consumer-tools/auto-loans/',
    '/consumer-tools/credit-reports-and-scores/',
    '/consumer-tools/debt-collection/',
    '/consumer-tools/prepaid-cards/',
    '/consumer-tools/sending-money/',
    '/mortgagehelp/',
    '/consumer-tools/educator-tools/your-money-your-goals/',
    '/consumer-tools/educator-tools/adult-financial-education/',
    '/consumer-tools/educator-tools/youth-financial-education/',
    '/consumer-tools/educator-tools/library-resources/',
    '/consumer-tools/educator-tools/resources-for-tax-preparers/',
    '/consumer-tools/money-as-you-grow/',
    '/empowerment/',
    '/consumer-tools/educator-tools/resources-for-older-adults/',
    '/consumer-tools/educator-tools/youth-financial-education/',  # TDP
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
    '/rules-policy/',
    '/compliance/',
    '/compliance/implementation-guidance/',
    '/enforcement/',
    '/rules-policy/notice-opportunities-comment/',
    '/compliance/amicus/',
    '/compliance/implementation-guidance/hmda-implementation/',
    '/compliance/implementation-guidance/mortserv/',
    '/compliance/implementation-guidance/tila-respa-disclosure-rule/'
]

# call `set` on the combined list to weed out dupes
FALLBACK_URLS = sorted(set(TOP + APPS))


def get_full_list():
    """Fetch a list of URLs to test from github, or fall back to local default."""
    try:
        url_data = requests.get(GIT_URI).text.split('\n')
    except Exception as e:
        logger.warning(
            'Using fallback because request for S3 list failed: {}'.format(e))
        url_list = FALLBACK_URLS
    else:
        #github only has the top 20 URLS not the APPS so that will be hard coded
        url_list = sorted(set(url_data + APPS))
    return url_list


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

    ./cfgov/scripts/http_smoke_test.py -v --base 'http://localhost:8000' --url_list '/' '/retirement/before-you-claim/'  # noqa: E501
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
                logger.info("{} failed with status code {}".format(url, code))
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
