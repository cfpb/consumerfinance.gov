from __future__ import unicode_literals

import datetime
from dateutil import parser
import logging
import sys

import unicodecsv

from data_research.models import MortgageDataConstant, County
from data_research.mortgage_utilities.s3_utils import (
    read_in_s3_csv, S3_SOURCE_BUCKET, S3_SOURCE_FILE)
from data_research.mortgage_utilities.fips_meta import validate_fips

CSV_LOADER_NAME = 'mp_countydata.csv'  # file output to /tmp

logger = logging.getLogger(__name__)


def update_through_date_constant(date):
    constant, cr = MortgageDataConstant.objects.get_or_create(
        name='through_date')
    constant.date_value = date
    constant.save()


def create_csv(starting_date, through_date):
    """
    This is part of pipeline Step 1. It produces a headerless CSV that can be
    bulk-loaded into our Mysql db with `LOAD DATA INFILE`.
    The CSV is saved to `/tmp/mp_countydata.csv`

    Sample input CSV field_names and row:
    date,fips,open,current,thirty,sixty,ninety,other
    01/01/08,1001,268,260,4,1,0,3

    Sample output row aimed at the `data_research_countymortgagedata` table:
    1,01001,2008-01-01,268,260,4,1,0,3,2891
    """
    starter = datetime.datetime.now()
    counter = 0
    pk = 1
    rows_out = []
    source_url = "{}/{}".format(S3_SOURCE_BUCKET, S3_SOURCE_FILE)
    raw_data = read_in_s3_csv(source_url)
    for row in raw_data:
        sampling_date = parser.parse(row.get('date')).date()
        if sampling_date >= starting_date and sampling_date <= through_date:
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
    with open('/tmp/{}'.format(CSV_LOADER_NAME), 'w') as f:
        writer = unicodecsv.writer(f)
        for row in rows_out:
            writer.writerow(row)
    logger.info('\nprep_csv took {} to create a CSV with {} rows'.format(
        (datetime.datetime.now() - starter), len(rows_out)))


def run(*args):  # pragma: no cover
    """
    Pass in the through-date in YYYY-MM-DD format with:
    `--script-args 2017-03-01`
    """
    starting_year = MortgageDataConstant.objects.get(
        name='starting_year').value
    starting_date = datetime.date(starting_year, 1, 1)
    if args:
        through_date = parser.parse(args[0]).date()
        update_through_date_constant(through_date)
        create_csv(starting_date, through_date)
    else:
        logger.info("Please provide a through-date in this form: YYYY-MM-DD.")
