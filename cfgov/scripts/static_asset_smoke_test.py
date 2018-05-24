"""Check that static assets are available on consumerfinance.gov"""
import argparse
import logging
import sys
import time

import requests
from bs4 import BeautifulSoup as bs


logger = logging.getLogger('static_asset_smoke_tests')
logger.setLevel(logging.ERROR)
shell_log = logging.StreamHandler()
shell_log.setLevel(logging.INFO)
logger.addHandler(shell_log)
parser = argparse.ArgumentParser()
parser.add_argument(
    "sub_urls",
    nargs='*',
    help=("add any number of sub-urls to check, separated by spaces\n  "
          "Example: `python static_asset_smoke_test.py askcfpb retirement`")
)
parser.add_argument(
    "-v", "--verbose",
    action="store_true",
    help="set logging level to info to see all message output."
)
parser.add_argument(
    "--base",
    help="choose a server base other than www.consumerfinance.gov"
)

CFPB_BASE = 'https://www.consumerfinance.gov'


def check_static(url):
    """Check all static links on a cf.gov page"""

    count = 0
    failures = []
    soup = bs(requests.get(url).content, 'html.parser')
    static_js = [
        link.get('src') for link in soup.findAll('script') if
        link.get('src') and 'static' in link.get('src')
    ]
    static_images = [
        image.get('src') for image in soup.findAll('img') if
        image.get('src') and 'static' in image.get('src')
    ]
    static_css = [
        link.get('href') for link in soup.findAll('link') if
        link.get('href') and 'static' in link.get('href')
    ]
    static_links = static_js + static_images + static_css
    for link in static_links:
        count += 1
        if link.startswith('/'):
            final_url = "{}{}".format(CFPB_BASE, link)
        else:
            final_url = "{}{}".format(url, link)
        code = requests.get(final_url).status_code
        if code == 200:
            logger.info("checked {}".format(final_url))
        else:
            failures.append((link, code))
    if failures:
        return ("\x1B[91mLight FAIL!{} static links failed "
                "for {}: {}\x1B[0m\n".format(len(failures), url, failures))
    else:
        return ("\x1B[32m{} static links passed "
                "for {}\x1B[0m\n".format(count, url))


if __name__ == '__main__':
    fail = False
    start = time.time()
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
    if args.base:
        CFPB_BASE = args.base
    logger.info(check_static(CFPB_BASE))
    if args.sub_urls:
        for arg in args.sub_urls:
            msg = check_static("{}/{}/".format(CFPB_BASE, arg))
            if 'FAIL' in msg:
                fail = True
            logger.warning(msg)
    logger.info("{} took {} seconds to check {}\n".format(
        sys.argv[0],
        int(time.time() - start),
        CFPB_BASE)
    )
    if not fail:
        logger.info('\x1B[32mSUCCESS! All static links return 200.\x1B[0m')
    else:
        logger.warning("\x1B[91mLightFAIL! Some static links "
                       "didn't return 200.\x1B[0m")
