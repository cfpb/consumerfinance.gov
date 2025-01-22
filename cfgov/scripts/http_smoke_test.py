#!/usr/bin/env python
import argparse
import json
import logging
import os
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
# Parameterized Host, all 3 must be defined to be used, can define via envvar
parser.add_argument(
    "--schema", help="HTTP/S", default=os.getenv("CFGOV_SCHEMA")
)
parser.add_argument(
    "--host", help="DNS Hostname", default=os.getenv("CFGOV_HOST")
)
parser.add_argument(
    "--port", help="CFGOV Port", default=os.getenv("CFGOV_PORT")
)
parser.add_argument(
    "--url_list",
    type=str,
    nargs="+",
    help=(
        "You can provide a space-separated custom list "
        "of relative URLs to check."
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
parser.add_argument(
    "--headers",
    type=json.loads,
    help="A JSON object of extra request headers.",
)

TIMEOUT = 30
HEADERS = {}
ALLOWED_TIMEOUTS = 1
FULL = False
BASE = "https://www.consumerfinance.gov"
S3_URI = (
    "https://files.consumerfinance.gov/build/smoketests/smoketest_urls.json"  # noqa: E501
)

# Fall-back list of top 25 URLs, as of May 2024
# All URLs in the list should be canonical locations of the given pages,
# not redirects.
TOP = [
    "/",
    "/complaint/",
    "/find-a-housing-counselor/",
    "/housing/housing-insecurity/help-for-renters/get-help-paying-rent-and-bills/",
    "/learnmore/",
    "/consumer-tools/debt-collection/",
    "/consumer-tools/guide-to-filing-your-taxes/",
    "/ask-cfpb/what-should-i-do-when-a-debt-collector-contacts-me-en-1695/",
    "/ask-cfpb/how-do-i-negotiate-a-settlement-with-a-debt-collector-en-1447/",
    "/ask-cfpb/how-do-i-get-a-free-copy-of-my-credit-reports-en-5/",
    "/rules-policy/regulations/",
    "/about-us/newsroom/consumer-advisory-opportunity-to-cancel-student-loan-debt-ends-soon/",
    "/ask-cfpb/what-is-a-money-market-account-en-1007/",
    "/data-research/consumer-complaints/search/",
    "/about-us/newsroom/",
    "/enforcement/actions/",
    "/ask-cfpb/does-a-persons-debt-go-away-when-they-die-en-1463/",
    "/about-us/contact-us/",
    "/ask-cfpb/where-can-i-get-my-credit-scores-en-316/",
    "/ask-cfpb/what-is-a-reverse-mortgage-en-224/",
    "/ask-cfpb/how-do-i-get-my-money-back-after-i-discover-an-unauthorized-transaction-or-money-missing-from-my-bank-account-en-1017/",
    "/paying-for-college/student-loan-forgiveness/",
    "/ask-cfpb/what-do-i-need-to-know-if-im-thinking-about-consolidating-my-credit-card-debt-en-1861/",
    "/rules-policy/regulations/1026/",
    "/ask-cfpb/what-should-i-do-if-im-sued-by-a-debt-collector-or-creditor-en-334/",
]

# URLs for cfgov sub-apps that are expected to be present
# All URLs in the list should be canonical locations of the given pages,
# not redirects.
APPS = [
    "/about-us/blog/",
    "/about-us/budget-strategy/",
    "/about-us/careers/",
    "/about-us/careers/current-openings/",
    "/about-us/doing-business-with-us/",
    "/about-us/events/",
    "/about-us/newsroom/",
    "/activity-log/",
    "/ask-cfpb/",
    "/compliance/",
    "/compliance/amicus/",
    "/compliance/compliance-resources/mortgage-resources/hmda-reporting-requirements/",
    "/compliance/compliance-resources/mortgage-resources/mortserv/",
    "/compliance/compliance-resources/mortgage-resources/tila-respa-integrated-disclosures/",
    "/consumer-tools/auto-loans/",
    "/consumer-tools/credit-reports-and-scores/",
    "/consumer-tools/debt-collection/",
    "/consumer-tools/educator-tools/adult-financial-education/",
    "/consumer-tools/educator-tools/library-resources/",
    "/consumer-tools/educator-tools/resources-for-older-adults/",
    "/consumer-tools/educator-tools/resources-for-tax-preparers/",
    "/consumer-tools/educator-tools/servicemembers/",
    "/consumer-tools/educator-tools/your-money-your-goals/",
    "/consumer-tools/educator-tools/youth-financial-education/",
    "/consumer-tools/educator-tools/youth-financial-education/",
    "/consumer-tools/money-as-you-grow/",
    "/consumer-tools/prepaid-cards/",
    "/consumer-tools/retirement/before-you-claim/",
    "/consumer-tools/retirement/retirement-api/estimator/1-1-1970/99000/",
    "/consumer-tools/sending-money/",
    "/data-research/",
    "/data-research/cfpb-research-conference/",
    "/data-research/cfpb-researchers/",
    "/data-research/consumer-complaints/",
    "/data-research/consumer-complaints/search/api/v1/?size=1",
    "/data-research/consumer-credit-trends/",
    "/data-research/credit-card-data/",
    "/data-research/hmda/",
    "/data-research/mortgage-performance-trends/",
    "/data-research/research-reports/",
    "/enforcement/",
    "/enforcement/payments-harmed-consumers/",
    "/es/",
    "/es/herramientas-del-consumidor/jubilacion/antes-de-solicitar/",
    "/es/obtener-respuestas/",
    "/fair-lending/",
    "/know-before-you-owe/",
    "/mortgagehelp/",
    "/oah-api/rates/rate-checker?price=200000&loan_amount=180000&minfico=740&maxfico=759&state=AL&rate_structure=fixed&loan_term=30&loan_type=conf",
    "/paying-for-college/",
    "/paying-for-college2/understanding-your-financial-aid-offer/about-this-tool/",  # noqa: E501
    "/policy-compliance/",
    "/rules-policy/",
    "/rules-policy/competition-innovation/",
    "/rules-policy/notice-opportunities-comment/",
    "/your-story/",
]

# call `set` on the combined list to weed out dupes
URLS = sorted(set(TOP + APPS))


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

    ./cfgov/scripts/http_smoke_test.py -v --base 'http://localhost:8000' --url_list '/' '/retirement/before-you-claim/'
    """  # noqa
    count = 0
    timeouts = []
    failures = []
    starter = time.time()
    if not url_list:
        url_list = URLS
    for url_suffix in url_list:
        logger.info(url_suffix)
        count += 1
        url = f"{base}{url_suffix}"
        try:
            response = requests.get(url, timeout=TIMEOUT, headers=HEADERS)
            code = response.status_code
            if code == 200:
                pass
            else:
                logger.info(f"{url} failed with status code {code}")
                failures.append((url, code))
        except requests.exceptions.Timeout:
            logger.info(f"{url} timed out")
            timeouts.append(url)
        except requests.exceptions.ConnectionError as e:
            logger.info(f"{url} returned a connection error")
            failures.append((url, e))
        except requests.exceptions.RequestException as e:
            logger.info(f"{url} failed for '{e}'")
            failures.append((url, e))
    timer = int(time.time() - starter)
    logger.info(
        f"\n{sys.argv[0]} took {timer} seconds to check {count} "
        f"URLs at {base}\n  "
        f"{len(failures)} failed\n  "
        f"{len(timeouts)} timed out"
    )

    if failures:
        logger.error(f"These URLs failed: {failures}")
    if len(timeouts) > ALLOWED_TIMEOUTS:
        logger.error(
            f"These URLs timed out after {TIMEOUT} seconds: {timeouts}"
        )
    elif timeouts:
        logger.info(
            "{} allowed timeouts occurred:\n{}".format(
                len(timeouts), "\n".join(timeouts)
            )
        )

    if failures or len(timeouts) > ALLOWED_TIMEOUTS:
        logger.error("FAIL")
        return False

    logger.info("\x1b[32mAll URLs return 200. No smoke!\x1b[0m")
    return True


if __name__ == "__main__":  # pragma: nocover
    url_list = None
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
    if args.base:
        BASE = args.base
    if args.schema and args.host and args.port:
        BASE = f"{args.schema.lower()}://{args.host}:{args.port}"
    if args.url_list:
        url_list = args.url_list
    if args.timeout:
        TIMEOUT = int(args.timeout)
    if args.headers:
        HEADERS = args.headers
    if not check_urls(BASE, url_list=url_list):
        sys.exit(1)
