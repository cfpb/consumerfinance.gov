#!/usr/bin/env python

import argparse
import sys

import requests
from tablib import Dataset


def load_redirects(redirects_filename):
    csv = redirects_filename.endswith('.csv')
    mode = 'rt' if csv else 'rb'

    with open(redirects_filename, mode) as f:
        dataset = Dataset().load(f, format='csv' if csv else None)

    return [tuple(row[i].rstrip('*') for i in (5, 6)) for row in dataset]


def validate_redirects(redirects_filename, baseurl):
    failures = []

    for from_path, to_path in load_redirects(redirects_filename):
        print(f'Checking {from_path} -> {to_path}...', end='')
        response = requests.get(baseurl + from_path, allow_redirects=False)

        redirected = response.status_code in (301, 302)

        if not redirected:
            print('error!', response.status_code)
            failures.append((from_path, to_path))
            continue

        location = response.headers.get('location')

        if location != to_path:
            print('error! location:', location)
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

    args = parser.parse_args()
    validate_redirects(**vars(args))
