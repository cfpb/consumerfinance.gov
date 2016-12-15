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
    "--full",
    action="store_true",
    help=("If --full is used, the script will check all urls in our main nav, "
          "plus a selection of our most-visited pages.")
)
parser.add_argument(
    "-v", "--verbose",
    action="store_true",
    help="set logging level to info to see all message output."
)

FULL = False
TIMEOUT = 10
BASE = 'http://www.consumerfinance.gov'

FULL_RUN = [
    '/',
    '/es/',
    ('/es/obtener-respuestas/buscar'
     '?selected_facets=category_exact:enviar-dinero'),
    '/complaint/',
    '/learnmore/',
    '/askcfpb/',
    '/askcfpb/search',
    '/your-story/',
    '/students/',
    '/find-a-housing-counselor/',
    '/older-americans/',
    '/servicemembers/',
    '/consumer-tools/auto-loans/',
    '/paying-for-college/',
    ('/paying-for-college2/understanding-your-financial-aid-offer/'
     'about-this-tool/'),
    '/owning-a-home/',
    '/retirement/before-you-claim/',
    '/retirement/before-you-claim/es/',
    '/sending-money/',
    '/know-before-you-owe/',
    '/mortgagehelp/',
    '/fair-lending/',
    '/your-money-your-goals/',
    '/adult-financial-education/',
    '/youth-financial-education/',
    '/library-resources/',
    '/tax-preparer-resources/',
    '/money-as-you-grow/',
    '/empowerment/',
    '/managing-someone-elses-money/',
    '/data-research/',
    '/data-research/research-reports/',
    '/data-research/cfpb-research-conference/',
    '/data-research/consumer-complaints/',
    '/data-research/hmda/',
    '/data-research/credit-card-data/',
    '/policy-compliance/',
    '/policy-compliance/rulemaking/',
    '/policy-compliance/guidance/',
    '/policy-compliance/enforcement/',
    '/policy-compliance/notice-opportunities-comment/',
    '/policy-compliance/amicus/',
    '/policy-compliance/guidance/implementation-guidance/',
    '/about-us/',
    '/about-us/careers/current-openings/',
    '/about-us/the-bureau/',
    '/about-us/budget-strategy/',
    '/about-us/payments-harmed-consumers/',
    '/about-us/blog/',
    '/about-us/newsroom/',
    '/about-us/events/',
    '/about-us/careers/',
    '/about-us/doing-business-with-us/',
    '/about-us/advisory-groups/',
    '/about-us/project-catalyst/',
    '/about-us/contact-us/',
    '/about-us/the-bureau/',
    '/activity-log/',
]

SHORT_RUN = [
    '/',
    '/es/',
    '/complaint/',
    '/learnmore/',
    # '/askcfpb/',
    '/askcfpb/search',
    '/your-story/',
    '/students/',
    '/find-a-housing-counselor/',
    '/older-americans/',
    # '/servicemembers/',
    '/consumer-tools/auto-loans/',
    '/paying-for-college/',
    ('/paying-for-college2/understanding-your-financial-aid-offer/'
     'about-this-tool/'),
    '/owning-a-home/',
    '/retirement/before-you-claim/',
    # '/retirement/before-you-claim/es/',
    '/sending-money/',
    '/know-before-you-owe/',
    # '/mortgagehelp/',
    '/fair-lending/',
    # '/your-money-your-goals/',
    '/adult-financial-education/',
    # '/youth-financial-education/',
    '/library-resources/',
    # '/tax-preparer-resources/',
    '/money-as-you-grow/',
    # '/empowerment/',
    # '/managing-someone-elses-money/',
    # '/data-research/',
    # '/data-research/research-reports/',
    # '/data-research/cfpb-research-conference/',
    '/data-research/consumer-complaints/',
    '/data-research/hmda/',
    # '/data-research/credit-card-data/',
    '/policy-compliance/',
    # '/policy-compliance/rulemaking/',
    # '/policy-compliance/guidance/',
    # '/policy-compliance/enforcement/',
    # '/policy-compliance/notice-opportunities-comment/',
    # '/policy-compliance/amicus/',
    # '/policy-compliance/guidance/implementation-guidance/',
    '/about-us/',
    '/about-us/careers/current-openings/',
    # '/about-us/the-bureau/',
    # '/about-us/budget-strategy/',
    # '/about-us/payments-harmed-consumers/',
    # '/about-us/blog/',
    '/about-us/newsroom/',
    # '/about-us/events/',
    # '/about-us/careers/',
    # '/about-us/doing-business-with-us/',
    # '/about-us/advisory-groups/',
    # '/about-us/project-catalyst/',
    # '/about-us/contact-us/',
    # '/about-us/the-bureau/',
    '/activity-log/',
]


def check_urls(base, full=False):
    """
    A smoke test to make sure the main cfgov URLs are returning status 200.

    The full option tests every link in the main nav, plus most popular pages.
    """

    count = 0
    timeouts = []
    failures = []
    starter = time.time()
    if full:
        url_list = FULL_RUN
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
    if timeouts:
        logger.error("These URLs timed out after {} seconds: "
                     "{}".format(TIMEOUT, timeouts))
    if failures or timeouts:
        logger.error("FAIL")
    else:
        logger.info("\x1B[32mAll URLs return 200. No smoke!\x1B[0m")

if __name__ == '__main__':
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
    if args.base:
        BASE = args.base
    if args.full:
        FULL = True
    check_urls(BASE, full=FULL)
