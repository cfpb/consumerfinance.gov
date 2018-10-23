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

FULL_RUN = [
    '/',
    '/es/',
    ('/es/obtener-respuestas/buscar'
     '?selected_facets=category_exact:enviar-dinero'),
    '/learnmore/',
    '/complaint/',
    '/complaint/getting-started/',
    '/ask-cfpb/',
    '/askcfpb/1017/',
    '/askcfpb/135/',
    '/askcfpb/1447/',
    '/askcfpb/1695/',
    '/askcfpb/1791/',
    '/askcfpb/316/',
    '/askcfpb/44/',
    '/your-story/',
    '/students/',
    '/find-a-housing-counselor/',
    '/servicemembers/',
    '/consumer-tools/auto-loans/',
    '/paying-for-college/',
    ('/paying-for-college2/understanding-your-financial-aid-offer/'
     'about-this-tool/'),
    '/owning-a-home/',
    '/retirement/before-you-claim/',
    '/retirement/before-you-claim/es/',
    '/consumer-tools/credit-reports-and-scores/',
    '/consumer-tools/debt-collection/',
    '/consumer-tools/prepaid-cards/',
    '/know-before-you-owe/',
    '/mortgagehelp/',
    '/fair-lending/',
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
    '/about-us/',
    '/about-us/the-bureau/',
    '/about-us/budget-strategy/',
    '/about-us/payments-harmed-consumers/',
    '/about-us/blog/',
    '/about-us/newsroom/',
    '/about-us/events/',
    '/activity-log/',
    '/about-us/careers/',
    '/about-us/careers/current-openings/',
    '/about-us/doing-business-with-us/',
    '/about-us/advisory-groups/',
    '/about-us/innovation/',
    '/about-us/contact-us/',
    '/eregulations/',
    '/eregulations/1026',
]

# TODO: Document the logic for what gets included/excluded in short-run tests
SHORT_RUN = [
    '/',
    '/es/',
    # ('/es/obtener-respuestas/buscar'
    #  '?selected_facets=category_exact:enviar-dinero'),'/complaint/',
    '/learnmore/',
    # '/complaint/'
    '/ask-cfpb/',
    '/your-story/',
    '/students/',
    '/find-a-housing-counselor/',
    # '/servicemembers/',
    '/consumer-tools/auto-loans/',
    '/paying-for-college/',
    ('/paying-for-college2/understanding-your-financial-aid-offer/'
     'about-this-tool/'),
    '/owning-a-home/',
    '/retirement/before-you-claim/',
    # '/retirement/before-you-claim/es/',
    # '/consumer-tools/credit-reports-and-scores/',
    # '/consumer-tools/debt-collection/',
    # '/consumer-tools/prepaid-cards/',
    '/know-before-you-owe/',
    # '/mortgagehelp/',
    '/fair-lending/',
    '/sending-money/',
    # '/educational-resources/your-money-your-goals/',
    '/adult-financial-education/',
    # '/educational-resources/youth-financial-education/',
    '/practitioner-resources/library-resources/',
    # '/educational-resources/tax-preparer-resources/',
    '/consumer-tools/money-as-you-grow/',
    # '/empowerment/',
    '/practitioner-resources/resources-for-older-adults/',
    # '/data-research/',
    # '/data-research/research-reports/',
    # '/data-research/cfpb-research-conference/',
    '/data-research/consumer-complaints/',
    '/data-research/hmda/',
    # '/data-research/consumer-credit-trends/',
    # '/data-research/credit-card-data/',
    # '/data-research/cfpb-researchers/',
    '/policy-compliance/',
    # '/policy-compliance/rulemaking/',
    # '/policy-compliance/guidance/',
    # '/policy-compliance/guidance/implementation-guidance/',
    # '/policy-compliance/enforcement/',
    # '/policy-compliance/notice-opportunities-comment/',
    # '/policy-compliance/amicus/',
    '/about-us/',
    # '/about-us/the-bureau/',
    # '/about-us/budget-strategy/',
    # '/about-us/payments-harmed-consumers/',
    # '/about-us/blog/',
    '/about-us/newsroom/',
    # '/about-us/events/',
    '/activity-log/',
    # '/about-us/careers/',
    '/about-us/careers/current-openings/',
    # '/about-us/doing-business-with-us/',
    # '/about-us/advisory-groups/',
    # '/about-us/innovation/',
    # '/about-us/contact-us/',
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


if __name__ == '__main__':
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
