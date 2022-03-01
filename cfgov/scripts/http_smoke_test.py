#!/usr/bin/env python
import argparse
import logging
import sys
import time

import requests


logger = logging.getLogger("http_smoke_tests")
logger.setLevel(logging.FATAL)
shell_log = logging.StreamHandler()
shell_log.setLevel(logging.INFO)
logger.addHandler(shell_log)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--base", help="choose a server base other than www.consumerfinance.gov"
)
parser.add_argument(
    "--url_list",
    type=str,
    nargs="+",
    help=(
        "You can provide a space-separated custom list " "of relative URLs to check."
    ),
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Set logging level to info to see all message output.",
)
parser.add_argument(
    "-t",
    "--timeout",
    type=str,
    help="Set a timeout level, in seconds; the default is 30.",
)

TIMEOUT = 30
ALLOWED_TIMEOUTS = 1
FULL = False
BASE = "https://www.consumerfinance.gov"
S3_URI = "https://files.consumerfinance.gov/build/smoketests/smoketest_urls.json"  # noqa: B950

# Fall-back list of top 25 URLs, as of July 2, 2020, from hubcap/wiki
# All URLs in the list should be canonical locations of the given pages,
# not redirects.
TOP = [
    "/",  # home page
    "/about-us/blog/guide-covid-19-economic-stimulus-checks/",
    "/about-us/blog/guide-coronavirus-mortgage-relief-options/",
    "/find-a-housing-counselor/",
    "/complaint/",
    "/learnmore/",
    "/ask-cfpb/what-is-the-best-way-to-negotiate-a-settlement-with-a-debt-collector-en-1447/",  # noqa: B950
    "/coronavirus/",
    "/about-us/blog/guide-covid-19-economic-stimulus-checks/#qualify/",
    "/consumer-tools/prepaid-cards/",
    "/coronavirus/cares-act-mortgage-forbearance-what-you-need-know/",
    "/about-us/blog/economic-impact-payment-prepaid-card/",
    "/about-us/blog/what-you-need-to-know-about-student-loans-and-coronavirus-pandemic/",  # noqa: B950
    "/complaint/getting-started/",
    "/coronavirus/mortgage-and-housing-assistance/",
    "/ask-cfpb/what-is-forbearance-en-289/",
    "/about-us/blog/guide-covid-19-economic-stimulus-checks/#when/",
    "/ask-cfpb/what-should-i-do-when-a-debt-collector-contacts-me-en-1695/",
    "/about-us/blog/protect-yourself-financially-from-impact-of-coronavirus/",
    "/about-us/contact-us/",
    "/about-us/blog/guide-coronavirus-mortgage-relief-options/#relief-options/",  # noqa: B950
    "/coronavirus/managing-your-finances/economic-impact-payment-prepaid-debit-cards/",  # noqa: B950
    "/ask-cfpb/how-can-i-tell-who-owns-my-mortgage-en-214/",
    "/rules-policy/regulations/",
    "/ask-cfpb/what-is-a-debt-to-income-ratio-why-is-the-43-debt-to-income-ratio-important-en-1791/",  # noqa: B950
]

# URLs for cfgov sub-apps that are expected to be present
# All URLs in the list should be canonical locations of the given pages,
# not redirects.
APPS = [
    "/about-us/budget-strategy/",
    "/enforcement/payments-harmed-consumers/",
    "/about-us/blog/",
    "/about-us/newsroom/",
    "/about-us/events/",
    "/about-us/careers/",
    "/about-us/careers/current-openings/",
    "/about-us/doing-business-with-us/",
    "/rules-policy/innovation/",
    "/activity-log/",
    "/ask-cfpb/",
    "/your-story/",
    "/es/",
    "/es/obtener-respuestas/",
    "/students/",
    "/consumer-tools/educator-tools/servicemembers/",
    "/know-before-you-owe/",
    "/fair-lending/",
    "/paying-for-college/",
    "/paying-for-college2/understanding-your-financial-aid-offer/about-this-tool/",  # noqa: B950
    "/retirement/before-you-claim/",
    "/retirement/before-you-claim/es/",
    "/consumer-tools/auto-loans/",
    "/consumer-tools/credit-reports-and-scores/",
    "/consumer-tools/debt-collection/",
    "/consumer-tools/prepaid-cards/",
    "/consumer-tools/sending-money/",
    "/mortgagehelp/",
    "/consumer-tools/educator-tools/your-money-your-goals/",
    "/consumer-tools/educator-tools/adult-financial-education/",
    "/consumer-tools/educator-tools/youth-financial-education/",
    "/consumer-tools/educator-tools/library-resources/",
    "/consumer-tools/educator-tools/resources-for-tax-preparers/",
    "/consumer-tools/money-as-you-grow/",
    "/empowerment/",
    "/consumer-tools/educator-tools/resources-for-older-adults/",
    "/consumer-tools/educator-tools/youth-financial-education/",  # TDP
    "/data-research/",
    "/data-research/research-reports/",
    "/data-research/cfpb-research-conference/",
    "/data-research/consumer-complaints/",
    "/data-research/hmda/",
    "/data-research/hmda/for-filers",
    "/data-research/consumer-credit-trends/",
    "/data-research/credit-card-data/",
    "/data-research/cfpb-researchers/",
    "/data-research/mortgage-performance-trends/",
    "/policy-compliance/",
    "/rules-policy/",
    "/compliance/",
    "/compliance/implementation-guidance/",
    "/enforcement/",
    "/rules-policy/notice-opportunities-comment/",
    "/compliance/amicus/",
    "/compliance/implementation-guidance/hmda-implementation/",
    "/compliance/implementation-guidance/mortserv/",
    "/compliance/implementation-guidance/tila-respa-disclosure-rule/",
]

# call `set` on the combined list to weed out dupes
FALLBACK_URLS = sorted(set(TOP + APPS))


def get_full_list():
    """Fetch a list of URLs to test from s3, or fall back to local default."""
    try:
        url_data = requests.get(S3_URI).json()
    except Exception as e:
        logger.warning(
            "Using fallback because request for S3 list failed: {}".format(e)
        )
        url_list = FALLBACK_URLS
    else:
        url_list = sorted(set(url_data.get("top") + url_data.get("apps")))
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

    ./cfgov/scripts/http_smoke_test.py -v --base 'http://localhost:8000' --url_list '/' '/retirement/before-you-claim/'  # noqa: B950
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
        url = "{}{}".format(base, url_suffix)
        try:
            response = requests.get(url, timeout=TIMEOUT)
            code = response.status_code
            if code == 200:
                pass
            else:
                logger.info("{} failed with status code {}".format(url, code))
                failures.append((url, code))
        except requests.exceptions.Timeout:
            logger.info("{} timed out".format(url))
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
            sys.argv[0], timer, count, base, len(failures), len(timeouts)
        )
    )

    if failures:
        logger.error("These URLs failed: {}".format(failures))
    if len(timeouts) > ALLOWED_TIMEOUTS:
        logger.error(
            "These URLs timed out after {} seconds: " "{}".format(TIMEOUT, timeouts)
        )
    elif timeouts:
        logger.info(
            "{} allowed timeouts occurred:\n"
            "{}".format(len(timeouts), "\n".join(timeouts))
        )

    if failures or len(timeouts) > ALLOWED_TIMEOUTS:
        logger.error("FAIL")
        return False

    logger.info("\x1B[32mAll URLs return 200. No smoke!\x1B[0m")
    return True


if __name__ == "__main__":  # pragma: nocover
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
