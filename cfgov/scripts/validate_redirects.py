#!/usr/bin/env python

import argparse
import re
import sys

import requests
from tablib import Dataset


def load_redirects(redirects_filename, from_index, to_index):
    csv = redirects_filename.endswith('.csv')
    mode = 'rt' if csv else 'rb'

    with open(redirects_filename, mode) as f:
        dataset = Dataset().load(f, format='csv' if csv else None)

    return [
        tuple(row[i].rstrip('*') for i in (from_index, to_index))
        for row in dataset
    ]


def validate_redirects(redirects, baseurl):
    failures = []

    base_url_http_or_https = re.sub(r'^https?', 'https?', baseurl)
    strip_baseurl_re = re.compile(r'^' + base_url_http_or_https)

    for from_path, to_path in redirects:
        print(f'Checking {from_path} -> {to_path}...', end='')
        response = requests.get(baseurl + from_path, allow_redirects=False)

        redirected = response.status_code in (301, 302)

        if not redirected:
            print('error!', response.status_code)
            failures.append((from_path, to_path))
            continue

        location = response.headers.get('location')

        relative_location = strip_baseurl_re.sub('', location)

        if relative_location != to_path:
            print('error! location:', relative_location)
            failures.append((from_path, to_path))
            continue

        print('ok')

    if failures:
        print('\nFailures:')

        for from_path, to_path in failures:
            print(f'- {from_path} -> {to_path}')

        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'redirects_filename',
        help='Redirects filename (XLSX format)'
    )
    parser.add_argument(
        'baseurl',
        help='Base URL, defaults to %(default)s',
        default='https://www.consumerfinance.gov',
        nargs='?'
    )
    parser.add_argument(
        '--from-index',
        help='Column index for from path, defaults to %(default)s',
        type=int,
        default=5
    )
    parser.add_argument(
        '--to-index',
        help='Column index for to path, defaults to %(default)s',
        type=int,
        default=6
    )

    args = parser.parse_args()

    redirects = load_redirects(
        args.redirects_filename,
        args.from_index,
        args.to_index
    )

    validate_redirects(redirects, args.baseurl)
