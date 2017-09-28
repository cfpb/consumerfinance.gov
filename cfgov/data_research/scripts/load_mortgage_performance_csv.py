from __future__ import unicode_literals

import datetime
from dateutil import parser
import logging
import os
import sys

# from django.core.exceptions import ObjectDoesNotExist

from data_research.models import (
    MortgageDataConstant, County, CountyMortgageData)
from data_research.mortgage_utilities.s3_utils import read_in_s3_csv
from data_research.mortgage_utilities.fips_meta import validate_fips

S3_SOURCE_BUCKET = (
    'http://files.consumerfinance.gov.s3.amazonaws.com/'
    'data/mortgage-performance/source'
)

logger = logging.getLogger(__name__)
script = os.path.basename(__file__)

# sample CSV field_names and row:
# date,fips,open,current,thirty,sixty,ninety,other
# 01/01/98,1001,268,260,4,1,0,3


def load_values(s3_filename, starting_date, return_fips=False):
    """Drop and reload the CountyMortgageData table."""

    counter = 0
    source_url = "{}/{}".format(S3_SOURCE_BUCKET, s3_filename)
    logger.info("Deleting CountyMortgageData objects.")
    CountyMortgageData.objects.all().delete()
    logger.info("CountyMorgtgageData count is now {}".format(
        CountyMortgageData.objects.count()))
    raw_data = read_in_s3_csv(source_url)
    # raw_data is a generator delivering data dicts, each representing a row
    if return_fips is True:
        fips_list = [validate_fips(row.get('fips')) for row in raw_data]
        return sorted(set(fips_list))
    for row in raw_data:
        sampling_date = parser.parse(row.get('date')).date()
        if sampling_date >= starting_date:
            valid_fips = validate_fips(row.get('fips'))
            if valid_fips:
                county = County.objects.get(fips=valid_fips)
                obj = CountyMortgageData(
                    fips=valid_fips,
                    county=county,
                    date=sampling_date,
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
                    logger.info("\n{}".format(counter))
    logger.info("\nCreated {} CountyMortgageData objects".format(
        CountyMortgageData.objects.count()))


def run(*args):  # pragma: no cover
    """
    Pass in the S3 filename like so:
    `--script-args latest_county_delinquency.csv`
    """
    starter = datetime.datetime.now()
    starting_year = MortgageDataConstant.objects.get(
        name='starting_year').value
    starting_date = datetime.date(starting_year, 1, 1)
    if args:
        load_values(s3_filename=args[0], starting_date=starting_date)
        logger.info("{} took {} to run.".format(
            script, (datetime.datetime.now() - starter)))
    else:
        logger.info('You must provide an S3 filename to load.')
