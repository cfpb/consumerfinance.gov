from __future__ import unicode_literals

import json
import logging

from django.conf import settings
import unicodecsv

PROJECT_ROOT = settings.PROJECT_ROOT
FIPS_DATA_PATH = (
    "{}/data_research/data".format(PROJECT_ROOT))

# We have minimal data for territories, so we exclude all but Puerto Rico (72)
NON_STATES = {'MP': '69', 'AS': '60', 'VI': '78', 'GU': '66'}  # , 'PR': '72'}

# Census no longer uses these FIPS codes, but they show up in the NMDB data.
# For more details on stale FIPS and FIPS for territories, see
# [GHE]/CFGOV/mortgage-performance/wiki/Processing-of-source-file
STALE_FIPS = [
    '02201',  # Prince of Wales-Outer Ketchikan, AK
    '02231',  # Skagway-Yakutat-Angoon Census Area, AK, DELETED 1992-09-22
    '02232',  # Skagway-Hoonah-Angoon Census Area, AK, DELETED 2007-06-20
    '02270',  # Wade Hampton Census Area, AK
    '02280',  # Wrangell-Petersburg Census Area, AK, DELETED 2008-06-01
    '12151',  # anomaly with insignificant data
    '24057',  # anomaly with insignificant data
    '41113',  # anomaly with insignificant data
    '51560',  # Clifton Forge County, VA, DELETED 2001-07-01
    '51780',  # South Boston City, VA, DELETED 1995-06-30
]
# These codes refer to small U.S. territories that don't meet our threshold.
TERRITORIES_TO_IGNORE = [
    '60010',
    '66010',
    '69110',
    '69120',
    '78010',
    '78020',
    '78030',
]
IGNORE_FIPS = STALE_FIPS + TERRITORIES_TO_IGNORE

SOURCE_HEADINGS = [  # last changed 2017-07-31
    'date',
    'fips',
    'open',  # stored as `total` in database
    'current',
    'thirty',
    'sixty',
    'ninety',
    'other'
]

logger = logging.getLogger(__name__)


class FipsMeta(object):
    """A metadata reference for juggling mortgage records"""
    def __init__(self):
        self.county_fips = {}  # 3 mappings of FIPS to metadata
        self.state_fips = {}
        self.msa_fips = {}
        self.non_msa_fips = {}
        self.nation_row = {}  # storage placeholder for CSV downloads
        self.whitelist = []  # FIPS that meet our threshold for display
        self.all_fips = []  # All valid county, MSA and state FIPS
        self.dates = []  # All the sampling dates we're displaying; will grow
        self.short_dates = []  # Shortened date versions for output labels
        self.starting_year = None  # next 3 values will reflect db constants
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


def load_county_mappings():
    """Add lists of counties and non-MSA counties to state_fips attribute."""
    from data_research.models import MortgageMetaData
    msa_meta = MortgageMetaData.objects.get(name='state_msa_meta').json_value
    for each in FIPS.state_fips:
        _attr = FIPS.state_fips[each]
        abbr = _attr['abbr']
        _attr['counties'] = (
            [county_fips for county_fips in FIPS.county_fips
             if county_fips[:2] == each])
        _attr['msas'] = [entry['fips'] for entry in msa_meta[abbr]['metros']]
        _attr['msa_counties'] = []
        for msa in _attr['msas']:
            _attr['msa_counties'] += (
                [county for county in FIPS.msa_fips[msa]['county_list']
                 if county in _attr['counties']])
        _attr['msa_counties'] = sorted(set(_attr['msa_counties']))
        _attr['non_msa_counties'] = (
            [county for county in _attr['counties']
             if county not in _attr['msa_counties']]
        )


def load_fips_lists():
    from data_research.models import MortgageMetaData
    for attr in ['whitelist', 'all_fips']:
        setattr(FIPS, attr, MortgageMetaData.objects.get(name=attr).json_value)
    FIPS.state_fips = MortgageMetaData.objects.get(
        name='state_meta').json_value


def load_constants():
    """Get data thresholds from database, or fall back to starting defaults."""
    from data_research.models import MortgageDataConstant, MortgageMetaData
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
    try:
        dates_obj = MortgageMetaData.objects.get(name='sampling_dates')
        dates = dates_obj.json_value
    except MortgageMetaData.DoesNotExist:
        with open("{}/sampling_dates.json".format(FIPS_DATA_PATH), 'rb') as f:
            dates = json.loads(f.read())
    FIPS.dates = ['{}'.format(date) for date in dates]
    FIPS.short_dates = [date[:-3] for date in FIPS.dates]


def load_fips_meta(counties=True):
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
    load_fips_lists()
    if counties is True:
        load_county_mappings()
    load_constants()
