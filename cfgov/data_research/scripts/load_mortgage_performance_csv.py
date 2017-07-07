from __future__ import unicode_literals

from dateutil import parser
import StringIO
import sys

import requests
import unicodecsv

from django.conf import settings
from data_research.models import CountyMortgageData


OUTDATED_FIPS = {
    # These outdated FIPS codes show up in the mortgage data
    # and should be changed or ignored:
    '02201': '',  # Prince of Wales-Outer Ketchikan, AK
    '02270': '',  # Wade Hampton Census Area, AK
    '12025': '12086',  # Dade, which became Miami-Dade (12086) in 1990s
    '12151': '',  # FL (??) only shows up thru 2011
    '46113': '46102',  # Shannon County SD, renamed Oglala Lakota 2015-05-01
    '51560': '',  # Clifton Forge County, VA, DELETED 2001-07-01
    '51780': '',  # South Boston City, VA, DELETED 1995-06-30
    # These older codes should also be ignored if they are ever encountered:
    '02231': '',  # Skagway-Yakutat-Angoon Census Area, AK, DELETED 1992-09-22
    '02232': '',  # Skagway-Hoonah-Angoon Census Area, AK, DELETED 2007-06-20
    '02280': '',  # Wrangell-Petersburg Census Area, AK, DELETED 2008-06-01
}

LOCAL_ROOT = settings.PROJECT_ROOT
S3_BASE = (
    'http://files.consumerfinance.gov.s3.amazonaws.com/mortgage-performance')
BASE_DATA_URL = '{}/delinquency_county_long.csv'.format(S3_BASE)
FIPS_DATA_PATH = (
    "{}/data_research/data".format(LOCAL_ROOT))


def validate_fips(raw_fips):
    """
    Fix county FIPS code anomalies, handling illegal lengths, truncated codes
    that have lost their initial zeroes and a county that changed its name
    and FIPS code in May 2015.
    """
    if len(raw_fips) not in [4, 5]:
        return None
    if raw_fips == '46113':  # Fix Oglala Lakota County, SD
        return OUTDATED_FIPS['46113']
    if len(raw_fips) == 4:
        new_fips = "0{}".format(raw_fips)
    else:
        new_fips = raw_fips
    if new_fips in OUTDATED_FIPS:
        return None
    else:
        return new_fips


def read_in_s3(url):
    response = requests.get(url)
    f = StringIO.StringIO(response.content)
    reader = unicodecsv.DictReader(f)
    return reader

# CSV_HEADINGS = [
#     'month',
#     'date',
#     'fipstop',
#     'open',
#     'current',
#     'thirty',
#     'sixty',
#     'ninety',
#     'other']


def load_values():
    counter = 0
    print("Reading in data from s3 ...")
    raw_data = read_in_s3(BASE_DATA_URL)
    # raw_data is a generator delivering data dicts, each representing a row
    print("Data read; now creating database entries ...")
    for row in raw_data:
        valid_fips = validate_fips(row.get('fipstop'))
        if valid_fips:
            obj = CountyMortgageData(
                fips=valid_fips,
                date=parser.parse(row.get('date')).date(),
                total=int(row.get('open')),
                current=int(row.get('current')),
                thirty=int(row.get('thirty')),
                sixty=int(row.get('sixty')),
                ninety=int(row.get('ninety')),
                other=int(row.get('other')))
            obj.save()
            counter += 1
            if counter % 10000 == 0:  # pragma: no cover
                sys.stdout.write('.')
                sys.stdout.flush()
            if counter % 100000 == 0:  # pragma: no cover
                print("\n{}".format(counter))
    print("Created {} mortgage data rows".format(counter))


def run():
    load_values()
