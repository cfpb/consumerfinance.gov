import json
from collections import OrderedDict
from pathlib import Path


FIXTURES_DIR = Path(__file__).resolve().parents[2]
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


def get_national_stats():
    """return dictionary of national college statistics"""
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
