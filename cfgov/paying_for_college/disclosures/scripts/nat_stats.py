import json
import os
from collections import OrderedDict
from subprocess import call

import requests
import yaml
from unipath import Path


COLLEGE_CHOICE_NATIONAL_DATA_URL = (
    'https://raw.githubusercontent.com/RTICWDT/'
    'college-scorecard/dev/_data/national_stats.yaml'
)
FIXTURES_DIR = Path(__file__).ancestor(3)
NAT_DATA_FILE = '{0}/fixtures/national_stats.json'.format(FIXTURES_DIR)
BACKUP_FILE = '{0}/fixtures/national_stats_backup.json'.format(FIXTURES_DIR)
# source for BLS_FILE: http://www.bls.gov/cex/#tables_long
BLS_FILE = '{0}/fixtures/bls_data.json'.format(FIXTURES_DIR)
LENGTH_MAP = {'earnings': {2: 'median_earnings_l4', 4: 'median_earnings_4'},
              'completion': {2: 'completion_rate_l4', 4: 'completion_rate_4'}}


def get_bls_stats():
    """Deliver BLS spending stats stored in the repo."""
    try:
        with open(BLS_FILE, 'r') as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        data = {}
    return data


def get_stats_yaml():
    """grab national stats yaml from scorecard repo"""
    nat_dict = {}
    try:
        nat_yaml = requests.get(COLLEGE_CHOICE_NATIONAL_DATA_URL)
        if nat_yaml.ok and nat_yaml.text:
            nat_dict = yaml.safe_load(nat_yaml.text)
    except AttributeError:  # If response.text has no value
        return nat_dict
    except requests.exceptions.ConnectionError:  # If requests can't connect
        return nat_dict
    else:
        return nat_dict


def update_national_stats_file():
    """update local data file if scorecard stats are available"""
    nat_dict = get_stats_yaml()
    if nat_dict == {}:
        return "Could not update national stats from {0}".format(
            COLLEGE_CHOICE_NATIONAL_DATA_URL
        )
    else:  # pragma: no cover -- not testing os and open
        if os.path.isfile(NAT_DATA_FILE):
            call(["mv", NAT_DATA_FILE, BACKUP_FILE])
        with open(NAT_DATA_FILE, 'w') as f:
            f.write(json.dumps(nat_dict, sort_keys=True, indent=4))
        return "OK"


def get_national_stats(update=False):
    """return dictionary of national college statistics"""
    if update is True:
        update_msg = update_national_stats_file()
        if update_msg != "OK":
            print(update_msg)
    with open(NAT_DATA_FILE, 'r') as f:
        return json.loads(f.read())


def get_prepped_stats(program_length=None):
    """deliver only the national stats we need for worksheets"""
    full_data = get_national_stats()
    natstats = {
        'completionRateMedian':
            full_data['completion_rate']['median'],
        'completionRateMedianLow':
            full_data['completion_rate']['average_range'][0],
        'completionRateMedianHigh':
            full_data['completion_rate']['average_range'][1],
        'nationalSalary': full_data['median_earnings']['median'],
        'nationalSalaryAvgLow':
            full_data['median_earnings']['average_range'][0],
        'nationalSalaryAvgHigh':
            full_data['median_earnings']['average_range'][1],
        'repaymentRateMedian':
            full_data['repayment_rate']['median'],
        'monthlyLoanMedian':
            full_data['median_monthly_loan']['median'],
        'retentionRateMedian':
            full_data['retention_rate']['median'],
        'netPriceMedian':
            full_data['net_price']['median']
    }
    national_stats_for_page = OrderedDict()
    for key in sorted(natstats.keys()):
        national_stats_for_page[key] = natstats[key]
    if program_length:
        national_stats_for_page['completionRateMedian'] = (
            full_data[LENGTH_MAP['completion'][program_length]]['median'])
        national_stats_for_page['completionRateMedianLow'] = (
            full_data[LENGTH_MAP[
                'completion'][program_length]]['average_range'][0])
        national_stats_for_page['completionRateMedianHigh'] = (
            full_data[LENGTH_MAP[
                'completion'][program_length]]['average_range'][1])
        national_stats_for_page['nationalSalary'] = (
            full_data[LENGTH_MAP['earnings'][program_length]]['median'])
        national_stats_for_page['nationalSalaryAvgLow'] = (
            full_data[LENGTH_MAP[
                'earnings'][program_length]]['average_range'][0])
        national_stats_for_page['nationalSalaryAvgHigh'] = (
            full_data[LENGTH_MAP[
                'earnings'][program_length]]['average_range'][1])
    return national_stats_for_page
