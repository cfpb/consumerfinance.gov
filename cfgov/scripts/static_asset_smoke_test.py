#!/usr/bin/env python
"""Check that static assets are available on consumerfinance.gov."""

import argparse
import logging
import sys
import time

import requests
from bs4 import BeautifulSoup as bs


logger = logging.getLogger("static_asset_smoke_tests")
logger.setLevel(logging.ERROR)
shell_log = logging.StreamHandler()
shell_log.setLevel(logging.INFO)
logger.addHandler(shell_log)
parser = argparse.ArgumentParser()
parser.add_argument(
    "sub_urls",
    type=str,
    nargs="*",
    help=(
        "add any number of sub-urls to check, separated by spaces\n  "
        "Example: `python static_asset_smoke_test.py askcfpb retirement`"
    ),
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="set logging level to info to see all message output.",
)
parser.add_argument(
    "--base",
    type=str,
    help="choose a server base other than www.consumerfinance.gov",
)

CFPB_BASE = "https://www.consumerfinance.gov"


def extract_static_links(page_content):
    """Deliver the static asset links from a page source."""
    soup = bs(page_content, "html.parser")
    static_js = [
        link.get("src")
        for link in soup.findAll("script")
        if link.get("src") and "static" in link.get("src")
    ]
    static_images = [
        image.get("src")
        for image in soup.findAll("img")
        if image.get("src") and "static" in image.get("src")
    ]
    static_css = [
        link.get("href")
        for link in soup.findAll("link")
        if link.get("href") and "static" in link.get("href")
    ]
    return static_js + static_images + static_css


def check_static(url):
    """
    Check viability of static links on cf.gov home page and sub-pages.

    Example call to check static assets in production:
    ./cfgov/scripts/static_asset_smoke_test.py -v /ask-cfpb/ /owning-a-home/

    Example of local check of home page:
    ./cfgov/scripts/static_asset_smoke_test.py -v --base http://localhost:8000
    """
    count = 0
    failures = []
    response = requests.get(url)
    if not response.ok:
        return f"\x1b[91mFAIL! Request to {url} failed ({response.reason})"
    static_links = extract_static_links(response.content)
    for link in static_links:
        count += 1
        if link.startswith("/"):
            final_url = f"{CFPB_BASE}{link}"
        else:
            final_url = f"{url}{link}"
        code = requests.get(
            final_url, headers={"referer": CFPB_BASE}
        ).status_code
        if code == 200:
            logger.info(f"checked {final_url}")
        else:
            failures.append((link, code))
    if failures:
        if len(failures) > 2:  # allow for font failures when testing locally
            return (
                f"\x1b[91mFAIL! {len(failures)} static links out of {count} "
                f"failed for {url}: {failures}\x1b[0m\n"
            )
        else:
            return (
                f"\x1b[91mPartial failure: {len(failures)} static links out "
                f"of {count} failed for {url}: {failures}\x1b[0m\n"
            )
    else:
        return f"\x1b[32m{count} static links passed for {url}\x1b[0m\n"


if __name__ == "__main__":  # pragma: nocover
    fail = False
    start = time.time()
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
    if args.base:
        CFPB_BASE = args.base
    base_msg = check_static(CFPB_BASE)
    if "FAIL!" in base_msg:
        logger.warning(base_msg)
        fail = True
    else:
        logger.info(base_msg)
    if args.sub_urls:
        for arg in args.sub_urls:
            sub_msg = check_static(f"{CFPB_BASE}{arg}")
            if "FAIL!" in sub_msg:
                fail = True
                logger.warning(sub_msg)
            else:
                logger.info(sub_msg)
    logger.info(
        f"{sys.argv[0]} took {int(time.time() - start)} seconds to check "
        f"{CFPB_BASE}\n"
    )
    if fail:
        logger.warning(
            "\x1b[91mFAIL. Too many static links didn't return 200.\x1b[0m"
        )
    else:
        logger.info("\x1b[32mSUCCESS! Static links return 200.\x1b[0m")
