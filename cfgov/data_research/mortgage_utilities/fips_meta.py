from __future__ import unicode_literals

import json

from django.conf import settings
import unicodecsv

PROJECT_ROOT = settings.PROJECT_ROOT
FIPS_DATA_PATH = (
    "{}/data_research/data".format(PROJECT_ROOT))
SOURCE_CSV_URL = (
    'http://files.consumerfinance.gov.s3.amazonaws.com/'
    'data/mortgage-performance/source/delinquency_county_0916.csv'
)

# We have minimal data for territories, so we exclude all but Puerto Rico (72)
NON_STATES = {'MP': '69', 'AS': '60', 'VI': '78', 'GU': '66'}  # , 'PR': '72'}


OUTDATED_FIPS = {
    # These outdated FIPS codes can show up in the mortgage data and should be
    # ignored, except for Shannon County, SD, which should be changed.
    '02201': '',  # Prince of Wales-Outer Ketchikan, AK
    '02270': '',  # Wade Hampton Census Area, AK
    '12025': '',  # Dade, which became Miami-Dade (12086) in 1990s
    '12151': '',  # FL (??) only shows up thru 2011
    '46113': '46102',  # Shannon County SD, renamed Oglala Lakota 2015-05-01
    '51560': '',  # Clifton Forge County, VA, DELETED 2001-07-01
    '51780': '',  # South Boston City, VA, DELETED 1995-06-30
    # These older codes should also be ignored if they are ever encountered:
    '02231': '',  # Skagway-Yakutat-Angoon Census Area, AK, DELETED 1992-09-22
    '02232': '',  # Skagway-Hoonah-Angoon Census Area, AK, DELETED 2007-06-20
    '02280': '',  # Wrangell-Petersburg Census Area, AK, DELETED 2008-06-01
}

SOURCE_HEADINGS = [  # last changed 2017-07-31
    'date',
    'fips',
    'open',
    'current',
    'thirty',
    'sixty',
    'ninety',
    'other'
]

OUTPUT_HEADINGS = [  # These have not been finalized
    'date',
    'fips',
    'state',
    'county',
    'msa',
    'open_num',
    'current_num',
    '30_60_days_delinquent_num',
    '30_60_days_delinquent_percent',
    '90_days_delinquent_num',
    '90_days_delinquent_percent',
    'other_num']


class FipsMeta(object):
    """A metadata reference for juggling mortgage records"""
    def __init__(self):
        self.county_fips = {}  # 3 mappings of FIPS to metadata
        self.state_fips = {}
        self.msa_fips = {}
        self.nation_row = {}  # storage placeholder for CSV downloads
        self.whitelist = []  # FIPS that meet our threshold for display
        self.all_fips = []  # All valid county, MSA and state FIPS
        self.dates = []  # All the sampling dates we're displaying; will grow
        self.short_dates = []  # Shortened date versions for output labels
        self.starting_date = None  # next 3 values will reflect db constants
        self.threshold_date = None
        self.threshold_count = None
        self.created = 0  # final 2 can serve as a global counters
        self.updated = 0

FIPS = FipsMeta()


def assemble_msa_mapping(msa_data):
    """
    Builds a dictionary of MSA IDs that are mapped to a list of county FIPS
    codes that belong to the MSA and to the MSA's name and included states.

    MSA IDs are not strictly FIPS codes, but we call them FIPS to keep the keys
    consistent when handling counties, MSAs and states.
    """
    def clean_name(data_row):
        raw_msa = data_row.get('msa_name')
        return raw_msa.replace('(Metropolitan Statistical Area)', '').strip()

    mapping = {row.get('msa_id').strip():
               {'county_list': [],
                'msa': clean_name(row),
                'name': clean_name(row)}  # dupe is for backward-compatibility
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
        FIPS.whitelist = json.loads(f.read())
        FIPS.whitelist.append('00000')


def load_all_fips():
    with open("{}/all_fips.json".format(FIPS_DATA_PATH), 'rb') as f:
        FIPS.all_fips = json.loads(f.read())
        FIPS.all_fips.append('00000')


def load_dates():
    with open("{}/sampling_dates.json".format(FIPS_DATA_PATH), 'rb') as f:
        FIPS.dates = json.loads(f.read())
        FIPS.short_dates = [date[:-3] for date in FIPS.dates]


def load_states():
    with open("{}/state_meta.json".format(FIPS_DATA_PATH), 'rb') as f:
        FIPS.state_fips = json.loads(f.read())


def load_thresholds():
    """Get data thresholds from database, or fall back to starting defaults."""
    from data_research.models import MortgageDataConstant
    threshold_defaults = {
        'starting_year': 2008,
        'threshold_count': 1000,
        'threshold_year': 2016,
    }
    for name in threshold_defaults:
        try:
            value = MortgageDataConstant.objects.get(
                name=name).value
        except MortgageDataConstant.DoesNotExist:
            value = threshold_defaults[name]
        setattr(FIPS, name, value)


def load_fips_meta():
    """
    Load FIPS mappings, starting with base CSV files.

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
                                     'fips': row['complete_fips'],
                                     'state': row['state'],
                                     'name': row['county_name'],
                                     }
                                    for row in fips_data
                                    if row['state'] not in NON_STATES}
            else:
                FIPS.msa_fips = assemble_msa_mapping(fips_data)
    load_dates()
    load_states()
    load_all_fips()
    load_whitelist()
    load_thresholds()


# Pipeline scripts


def validate_geo(geo, fips, year, count):
    """
    A utility to check whether a county, MSA or state had an average
    monthly mortgage count in our reference year to qualify for being
    included in visualizations.
    """
    from data_research.models import (
        CountyMortgageData, MSAMortgageData, StateMortgageData)
    qsets = {
        'county': CountyMortgageData.objects.filter(
            date__year=year, fips=fips),
        'msa': MSAMortgageData.objects.filter(
            date__year=year, fips=fips),
        'state': StateMortgageData.objects.filter(
            date__year=year, fips=fips)
    }
    records = qsets[geo]
    msum = sum([record.total for record in records if record.total])
    if records.count() != 0:
        avg = round((msum * 1.0) / records.count())
    else:
        avg = 0
    if avg > count:
        return True
    else:
        return False


def update_valid_geos():
    """
    For counties, metro areas and states, we need to include them
    in visualizations only if they meet our threshold.

    The threshold (initially 1K mortgages a month) is applied to the area's
    average for the threshold year, which is generally the previous year.

    This should be run once a year to rebuild the list of valid FIPS codes
    for visualizations. The list will be saved in the cfgov-refresh repo
    at `data_research/data/fips_whitelist.json` and can be consulted at
    runtime at FIPS.whitelist`
    """
    load_fips_meta()  # this loads the FIPS metadata object
    county_list = []
    msa_list = []
    state_list = []
    for fips in FIPS.county_fips:
        if validate_geo(
                'county', fips, FIPS.threshold_year, FIPS.threshold_count):
            county_list.append(fips)
    for fips in FIPS.msa_fips:
        if validate_geo(
                'msa', fips, FIPS.threshold_year, FIPS.threshold_count):
            msa_list.append(fips)
    for fips in FIPS.state_fips:
        if validate_geo(
                'state', fips, FIPS.threshold_year, FIPS.threshold_count):
            state_list.append(fips)
    final_list = sorted(state_list) + sorted(msa_list) + sorted(county_list)
    with open('{}/fips_whitelist.json'.format(FIPS_DATA_PATH), 'wb') as f:
        f.write(json.dumps(final_list))

    pct_values = {
        'counties': round(len(county_list) * 100 / len(FIPS.county_fips)),
        'msas': round(len(msa_list) * 100 / len(FIPS.msa_fips))}

    message = (
        "In {}, {} percent of counties and {} percent of MSAs met our "
        "mortgage-count threshold for visualizations.".format(
            FIPS.threshold_year,
            pct_values['counties'],
            pct_values['msas']))

    return message
