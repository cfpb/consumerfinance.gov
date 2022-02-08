import csv
import logging

from django.conf import settings


PROJECT_ROOT = settings.PROJECT_ROOT
FIPS_DATA_PATH = (
    "{}/data_research/data".format(PROJECT_ROOT))

# We have minimal data for smaller territories, so we exclude them.
# For project launch, we also excluded Puerto Rico (72) as out of scope.
NON_STATES = {'MP': '69', 'AS': '60', 'VI': '78', 'GU': '66', 'PR': '72'}

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

# These codes refer to small U.S. territories that don't meet our threshold
TERRITORIES_TO_IGNORE = [
    '60010',
    '66010',
    '69100',
    '69110',
    '69120',
    '78010',
    '78020',
    '78030',
]

PUERTO_RICO_COUNTIES = [
    '72071', '72027', '72073', '72029', '72103', '72105', '72085', '72129',
    '72109', '72031', '72033', '72035', '72037', '72097', '72095', '72139',
    '72091', '72045', '72041', '72093', '72153', '72099', '72023', '72025',
    '72079', '72075', '72077', '72047', '72043', '72125', '72123', '72049',
    '72121', '72069', '72067', '72065', '72063', '72061', '72059', '72053',
    '72051', '72057', '72055', '72054', '72083', '72101', '72107', '72081',
    '72087', '72089', '72149', '72039', '72019', '72017', '72013', '72007',
    '72133', '72131', '72135', '72137', '72009', '72001', '72003', '72005',
    '72151', '72127', '72117', '72115', '72145', '72015', '72147', '72141',
    '72011', '72143', '72113', '72111', '72119', '72021',
]

# Puerto Rico was initially out of scope.
# To add it to the data set, remove PUERTO_RICO_COUNTIES from IGNORE_FIPS
IGNORE_FIPS = STALE_FIPS + TERRITORIES_TO_IGNORE + PUERTO_RICO_COUNTIES

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


class FipsMeta:
    """A metadata reference for juggling mortgage records"""
    def __init__(self):
        self.county_fips = {}  # 3 mappings of FIPS to metadata
        self.state_fips = {}
        self.msa_fips = {}
        self.non_msa_fips = {}
        self.nation_row = {}  # storage placeholder for CSV downloads
        self.allowlist = []  # FIPS that meet our threshold for display
        self.all_fips = []  # All valid county, MSA and state FIPS
        self.dates = []  # All the sampling dates we're displaying; will grow
        self.short_dates = []  # Shortened date versions for output labels
        self.starting_date = None  # next 3 values will reflect db constants
        self.threshold_date = None
        self.threshold_count = None
        self.created = 0  # final 2 can serve as a global counters
        self.updated = 0


FIPS = FipsMeta()


def validate_fips(raw_fips, keep_outdated=False):
    """
    Fix anomalies in county FIPS codes, handling illegal lengths,
    truncated codes that have lost their initial zeroes and a county changed
    names and FIPS codes.
    """
    FIPS_SWAP = {
        '46113': '46102',  # Change Shannon County, SD, to Oglala Lakota
        # '12025': '12086'  # Dade/Miami-Dade is handled by merge_the_dades
    }
    if len(raw_fips) not in [4, 5]:
        return None
    if raw_fips in FIPS_SWAP:
        return FIPS_SWAP[raw_fips]
    if len(raw_fips) == 4:
        new_fips = "0{}".format(raw_fips)
    else:
        new_fips = raw_fips
    if keep_outdated is False and new_fips in IGNORE_FIPS:
        return None
    else:
        return new_fips


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
    live_fips = [fips for fips in FIPS.state_fips
                 if fips not in NON_STATES.values()]
    for each in live_fips:
        _attr = FIPS.state_fips[each]
        abbr = _attr['abbr']
        _attr['counties'] = (
            [county_fips for county_fips in FIPS.county_fips
             if county_fips[:2] == each])
        _attr['msas'] = [entry['fips']
                         for entry in msa_meta[abbr]['metros']
                         if 'non' not in entry['fips']]
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
    for attr in ['allowlist', 'all_fips']:
        setattr(FIPS, attr, MortgageMetaData.objects.get(name=attr).json_value)
    FIPS.state_fips = MortgageMetaData.objects.get(
        name='state_meta').json_value


def load_constants():
    """Get data thresholds."""
    from data_research.models import MortgageDataConstant, MortgageMetaData
    FIPS.starting_date = MortgageDataConstant.objects.get(
        name='starting_date').date_value
    for threshold in ['threshold_count', 'threshold_year']:
        value = MortgageDataConstant.objects.get(name=threshold).value
        setattr(FIPS, threshold, value)
    dates = MortgageMetaData.objects.get(name='sampling_dates').json_value
    FIPS.dates = ['{}'.format(date) for date in dates]
    FIPS.short_dates = [date[:-3] for date in FIPS.dates]


def load_fips_meta(counties=True):
    """`
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
        with open("{}/{}".format(FIPS_DATA_PATH, filename), 'r') as f:
            reader = csv.DictReader(f)
            fips_data = list(reader)
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
