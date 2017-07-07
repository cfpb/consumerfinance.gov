from __future__ import unicode_literals
# import datetime
# from dateutil import parser
# from decimal import Decimal
import json
import os
# import StringIO

# import requests
import boto
from boto.s3.connection import OrdinaryCallingFormat
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
# from rest_framework.settings import api_settings
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
# from rest_framework_csv import renderers as r
import unicodecsv

from django.conf import settings
from data_research.models import CountyMortgageData, MSAMortgageData
# from django.utils.functional import cached_property
# from rest_framework import authentication, permissions

# from data_research.utils.csvkit import DictReader as cdr

# Refs for outdated counties:
# https://www.census.gov/geo/reference/county-changes.html
# https://www.cdc.gov/nchs/data/nvss/bridged_race/county_geography_changes.pdf

S3_KEY = os.getenv('S3_KEY')
S3_SECRET = os.getenv('S3_SECRET')
s3_base = "http://files.consumerfinance.gov"  # not using ssl for s3
keyname = "data/mortgage-performance/metro"
# post to http://s3.amazonaws.com/files.consumerfinance.gov/
# data/mortgage-performance/msa/78030_90_day_delinq_percent.json
# data/mortgage-performance/msa/78030_30_day_delinq_percent.json


def prep_key(key, content):
    """Prep content for an s3 endpoint 'key'."""
    key.set_contents_from_string(content)
    key.set_acl('public-read')
    key.content_type = 'application/json'
    return key


def bake_msa_to_s3(fips, day_range, json_string):
    from boto.s3.key import Key
    s3 = boto.connect_s3(S3_KEY,
                         S3_SECRET,
                         calling_format=OrdinaryCallingFormat())
    bucket = s3.get_bucket('files.consumerfinance.gov')
    json_prep = Key(
        bucket=bucket, name='{}/{}_{}_day_delinq_percent.json'.format(
            keyname, fips, day_range))
    json_prep = prep_key(json_prep, json_string)


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

ORIGINAL_HEADINGS = [
    'month',
    'date',
    'fipstop',
    'open',
    'current',
    'thirty',
    'sixty',
    'ninety',
    'other']

OUTPUT_HEADINGS = [
    'date',
    'fips',
    'state',
    'county',
    'msa',
    'open_num',
    'current_num',
    '30_days_delinquent_num',
    '30_days_delinquent_percent',
    '90_days_delinquent_num',
    '90_days_delinquent_percent',
    'other_num']

state_names = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

# We have minimal data for these, so we exclude; Puerto Rico is the exception
205472

NON_STATES = {'MP': '69', 'AS': '60', 'VI': '78', 'GU': '66'}  # , 'PR': '72'}

LOCAL_ROOT = settings.PROJECT_ROOT
FIPS_DATA_PATH = (
    "{}/data_research/data".format(LOCAL_ROOT))


class FipsMeta():
    def __init__(self):
        self.county_fips = {}
        self.state_fips = {}
        self.msa_fips = {}
        self.fips_whitelist = []
        self.dates = []

FIPS = FipsMeta()


def assemble_msa_mapping(msa_data):
    """
    Builds a dictionary of MSA IDs that are mapped to a list
    of county FIPS codes that belong to the MSA and the MSA's name and state.
    """
    def clean_name(data_row):
        raw_msa = data_row.get('msa_name')
        return raw_msa.replace('(Metropolitan Statistical Area)', '').strip()

    mapping = {row.get('msa_id').strip():
               {'county_list': [], 'msa': clean_name(row)}
               for row in msa_data
               if row.get('msa_id').strip()}
    for msa_id in mapping:
        mapping[msa_id]['fips'] = msa_id
        mapping[msa_id]['county_list'] += [row.get('county_fips')
                                           for row in msa_data
                                           if row.get('msa_id') == msa_id]
    return mapping


def load_whitelist():
    with open("{}/fips_whitelist.json".format(FIPS_DATA_PATH), 'rb') as f:
        FIPS.fips_whitelist = json.loads(f.read())


def load_dates():
    with open("{}/sampling_dates.json".format(FIPS_DATA_PATH), 'rb') as f:
        FIPS.dates = json.loads(f.read())


def load_fips_meta():
    """
    Load FIPS mappings from CSV files.

    County CSV headings are:
        1: state
        2: state_fips
        3: county_fips
        4: complete_fips
        5: county_name

    MSA CSV headings are:
        1: msa_id
        2: msa_name
        3: county_fips
        4: county_name
    """
    for filename in ['state_county_fips.csv', 'msa_county_crosswalk.csv']:
        with open("{}/{}".format(FIPS_DATA_PATH, filename), 'rb') as f:
            reader = unicodecsv.DictReader(f)
            fips_data = [row for row in reader]
            if 'state' in filename:
                FIPS.county_fips = {row['complete_fips']:
                                    {'county': row['county_name'],
                                    'state': row['state']}
                                    for row in fips_data}
    #                                if row['state'] not in NON_STATES}
                FIPS.state_fips = {row['state_fips']: row['state']
                                   for row in fips_data}
            else:
                FIPS.msa_fips = assemble_msa_mapping(fips_data)
    load_whitelist()
    load_dates()


# def convert_date_to_epoch(date_string):
#     date = parser.parse(date_string)
#     if date.date() == datetime.date.today():
#         raise ValueError("Invalid date supplied")
#     return int(date.strftime('%s'))


def parse_raw_fips(raw_fips):
    """Return a dict of valid state, county and combined FIPS combinations."""
    load_fips_meta()
    fips_dict = {'national': False,
                 'msa': '',
                 'msa_fips': '',
                 'state': '',
                 'state_fips': '',
                 'county': '',
                 'county_fips': ''}
    if raw_fips == '00000':
        fips_dict['national'] = FIPS.state_fips.keys()
        return fips_dict
    if raw_fips == '46113':
        raw_fips = '46102'  # Fixes Oglala Lakota County, SD
    if raw_fips in FIPS.msa_fips.keys():
        msa_data = FIPS.msa_fips.get(raw_fips)
        fips_dict['msa'] = msa_data.get('')
    if len(raw_fips) in [1, 2]:
        if len(raw_fips) == 1:
            state_fips = "0{}".format(raw_fips)
        else:
            state_fips = raw_fips
        fips_dict['state'] = FIPS.state.get(state_fips)
        fips_dict['state_fips'] = state_fips
        return fips_dict
    if len(raw_fips) == 4:
        raw_fips = "0{}".format(raw_fips)
    if len(raw_fips) == 5:
        if not FIPS.county.get(raw_fips):
            if raw_fips not in FIPS.missing:
                FIPS.missing.append(raw_fips)
            print("Coudln't find a county for {}".format(raw_fips))
        state_fips = raw_fips[:2]
        fips_dict['state_fips'] = state_fips
        fips_dict['county_fips'] = raw_fips
        fips_dict['state'] = FIPS.state[state_fips]
        fips_dict['county'] = FIPS.county.get(raw_fips)
        return fips_dict
    else:
        raise ValidationError("Invalid FIPS code")


# def convert_row(original_row):
#     """Convert a dict-based row of original data to reader-friendly row"""
#     fips_dict = parse_raw_fips(original_row['fipstop'])
#     delinquedict = calculate_percentages([original_row])
#     new_row = {
#         'date': original_row['date'],
#         'fips': fips_dict['county_fips'],
#         'state': fips_dict['state'],
#         'county': fips_dict['county'],
#         'msa': '',
#         'open_num': original_row['open'],
#         'current_num': original_row['current'],
#         '30_days_delinquent_num': delinquedict['30_days'],
#         '30_days_delinquent_percent': delinquedict['30_day_pct'],
#         '90_days_delinquent_num': delinquedict['90_days'],
#         '90_days_delinquent_percent': delinquedict['90_day_pct'],
#         'other_num': original_row['other']
#     }
#     return new_row


# def read_in_s3(url):
#     data = [{}]
#     response = requests.get(url)
#     try:
#         f = StringIO.StringIO(response.content)
#         reader = unicodecsv.DictReader(f, encoding='utf-8')
#         data = [row for row in reader]
#     except UnicodeDecodeError:
#         f = StringIO.StringIO(response.content)
#         reader = unicodecsv.DictReader(f, encoding='windows-1252')
#         data = [row for row in reader]
#     except:
#         return data
#     return data


# def convert_csv():
#     """
#     Read in the base CSV file, fix FIPS codes to restore leading zeroes
#     and skip outdated FIPS codes (ones that no longer exist),
#     and output a CSV with reader-friendly column headings.
#     """
#     raw_data = read_in_s3(BASE_DATA_URL)
#     # outfile = StringIO.StringIO()
#     with open('converted_mortgage_data.csv', 'wb') as f:
#         writer = unicodecsv.writer(f)
#         writer.writerow(OUTPUT_HEADINGS)
#         for raw in raw_data:
#             row = convert_row(raw)
#             if row['fips'] not in OUTDATED_FIPS:
#                 writer.writerow([row[headng] for headng in OUTPUT_HEADINGS])


def national_time_series():

    return "National time series is not yet implemented."


def time_series_by_fips(fips):
    """
    Deliver a time series of mortgage performance data for a geo slice.
    A FIPS code can identify a state, county or MSA. For our purposes,
    the nationwide slice is returned for a FIPS code of '00000'.
    """
    if fips == '00000':
        return national_time_series()
    else:
        pass


class TimeSeriesData(APIView):
    """
    View for delivering geo-based time-series data
    from the mortgage performance dataset.
    """
    renderer_classes = (JSONRenderer,)  # , r.CSVRenderer)

    # def print_format(self, **kwargs):
    #     print(self.get_format_suffix(**kwargs))

    def get(self, request, fips, format='json'):
        """
        Return a FIPS-based slice of base data in json (default) or CSV format.
        """
        if fips == '00000':
            return Response(national_time_series())
        load_fips_meta()
        if fips in FIPS.fips_whitelist:
            if fips in FIPS.county_fips:
                records = CountyMortgageData.objects.filter(fips=fips)
                name = "{}, {}".format(
                    FIPS.county_fips[fips]['county'],
                    FIPS.county_fips[fips]['state'])
                data = {'meta': {'fips': fips,
                                 'name': name,
                                 'fips_type': 'county'},
                        'data': [record.time_series for record in records]}
            else:
                records = MSAMortgageData.objects.filter(fips=fips)
                name = FIPS.msa_fips[fips]['msa']
                data = {'meta': {'fips': fips,
                                 'name': name,
                                 'fips_type': 'msa'},
                        'data': [record.time_series for record in records]}
                return Response(data)
        else:
            return Response("FIPS code not found")


class MapData(APIView):
    """
    View for delivering geo-based map data
    from the mortgage performance dataset.
    """
    renderer_classes = (JSONRenderer,)  # , r.CSVRenderer)

    def get(self, request, fips, format='json'):
        return Response("Not yet implemented")
