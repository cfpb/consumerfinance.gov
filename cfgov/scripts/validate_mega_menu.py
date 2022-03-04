#!/usr/bin/env python

import argparse
import re
import sys

import requests
from bs4 import BeautifulSoup


def validate_mega_menu(base):
    failures = []

    print(f"Retrieving mega menu from {base}")
    response = requests.get(base, allow_redirects=True)
    response.raise_for_status()

    html = response.content
    soup = BeautifulSoup(html, "html.parser")

    links = soup.findAll("a", {"class": "o-mega-menu_content-link"})
    for link in links:
        if "o-mega-menu_content-link__has-children" in link["class"]:
            continue

        text = link.text.strip()
        href = link["href"]

        print(f'Checking "{text}" ({href})...', end="")
        if not re.search(r"^https?://", href):
            href = base + href

        response = requests.get(href)

        if response.ok:
            print("ok")
        else:
            print("error!", response.status_code)
            failures.append((text, href))

    if failures:
        print("\nFailures:")

        for text, href in failures:
            print(f'- "{text}" ({href})"')

        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "base",
        help="Base URL, defaults to %(default)s",
        default="https://www.consumerfinance.gov",
        nargs="?",
    )

    args = parser.parse_args()
    validate_mega_menu(**vars(args))
