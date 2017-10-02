from __future__ import unicode_literals

import datetime
from dateutil import parser
import logging
import sys

import unicodecsv

from data_research.models import MortgageDataConstant, County
from data_research.mortgage_utilities.s3_utils import read_in_s3_csv
from data_research.mortgage_utilities.fips_meta import validate_fips


S3_SOURCE_BUCKET = (
    'http://files.consumerfinance.gov.s3.amazonaws.com/'
    'data/mortgage-performance/source'
)
CSV_NAME = 'mp_countydata.csv'  # file output to /tmp
DEFAULT_S3_SOURCE_FILE = 'latest_county_delinquency.csv'

logger = logging.getLogger(__name__)


def create_csv(s3_filename, starting_date):
    """
    Produce a header-less CSV that can loaded directly into a Mysql table with
    `LOAD DATA INFILE`. The CSV is saved to /tmp as `countydata.csv`

    sample input CSV field_names and row:
    date,fips,open,current,thirty,sixty,ninety,other
    01/01/08,1001,268,260,4,1,0,3

    sample output row aimed at the `data_research_countymortgagedata` table:
    1,01001,2008-01-01,268,260,4,1,0,3,2891
    """
    starter = datetime.datetime.now()
    counter = 0
    pk = 1
    rows_out = []
    source_url = "{}/{}".format(S3_SOURCE_BUCKET, s3_filename)
    raw_data = read_in_s3_csv(source_url)
    for row in raw_data:
        sampling_date = parser.parse(row.get('date')).date()
        if sampling_date >= starting_date:
            valid_fips = validate_fips(row.get('fips'))
            if valid_fips:
                county_pk = County.objects.get(fips=valid_fips).pk
                rows_out.append([
                    pk,
                    valid_fips,
                    "{}".format(sampling_date),
                    row.get('open'),
                    row.get('current'),
                    row.get('thirty'),
                    row.get('sixty'),
                    row.get('ninety'),
                    row.get('other'),
                    county_pk])
                pk += 1
                counter += 1
                if counter % 10000 == 0:  # pragma: no cover
                    sys.stdout.write('.')
                    sys.stdout.flush()
                if counter % 100000 == 0:  # pragma: no cover
                    logger.info("\n{}".format(counter))
    with open('/tmp/{}'.format(CSV_NAME), 'w') as f:
        writer = unicodecsv.writer(f)
        for row in rows_out:
            writer.writerow(row)
    logger.info('\nprep_csv took {} to create a CSV with {} rows'.format(
        (datetime.datetime.now() - starter), len(rows_out)))


def run(*args):  # pragma: no cover
    """
    Pass in the S3 filename like so:
    `--script-args latest_county_delinquency.csv`
    """
    starting_year = MortgageDataConstant.objects.get(
        name='starting_year').value
    starting_date = datetime.date(starting_year, 1, 1)
    if args:
        create_csv(s3_filename=args[0], starting_date=starting_date)
    else:
        create_csv(DEFAULT_S3_SOURCE_FILE, starting_date=starting_date)
