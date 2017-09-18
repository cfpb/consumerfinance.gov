from __future__ import unicode_literals

import datetime
from dateutil import parser
import json
import logging
import sys

from data_research.models import (
    MortgageDataConstant, MortgageMetaData, County, CountyMortgageData)
from data_research.mortgage_utilities.s3_utils import read_in_s3_csv
from data_research.mortgage_utilities.fips_meta import (
    FIPS_DATA_PATH, IGNORE_FIPS)

S3_SOURCE_BUCKET = (
    'http://files.consumerfinance.gov.s3.amazonaws.com/'
    'data/mortgage-performance/source'
)
ORIGINAL_FILENAME = 'delinquency_county_0317.csv'

logger = logging.getLogger(__name__)

# sample CSV field_names and row:
# date,fips,open,current,thirty,sixty,ninety,other
# 01/01/98,1001,268,260,4,1,0,3


def merge_the_dades():
    """
    Since the historical Dade County FIPS (12025) was redefined as
    Miami-Dade (12086) in the 1990s, we need to combine values for these two
    codes when mortgages assigned to the old FIPS show up in our base data.

    This routine adds values from a 12025 record to the current Miami-Dade
    record and deletes the outdated record so that the operation can't repeat.
    """
    fields = ['total', 'current', 'thirty', 'sixty', 'ninety', 'other']
    dade = CountyMortgageData.objects.filter(fips='12025')
    miami_dade = CountyMortgageData.objects.filter(fips='12086')
    for old_dade in dade:
        try:
            new_dade = miami_dade.get(date=old_dade.date)
        except CountyMortgageData.DoesNotExist:
            old_dade.delete()
        else:
            for field in fields:
                setattr(new_dade, field, (getattr(old_dade, field) +
                                          getattr(new_dade, field)))
            new_dade.save()  # this will recalculate the record's percentages
            old_dade.delete()
    logger.info("\nDade and Miami-Dade values merged.")


def update_sampling_dates():
    """
    Update our metadata list of sampling dates.
    """
    starting_year = MortgageDataConstant.objects.get(
        name='starting_year').value
    dates = sorted(set([obj.date for obj in CountyMortgageData.objects.filter(
        date__gte=datetime.date(starting_year, 1, 1))]))
    date_list = ["{}".format(date) for date in dates]
    date_list_obj, cr = MortgageMetaData.objects.get_or_create(
        name='sampling_dates')
    date_list_obj.json_value = json.dumps(date_list)
    date_list_obj.save()
    with open('{}/sampling_dates.json'.format(FIPS_DATA_PATH), 'wb') as f:
        f.write(json.dumps(date_list))
    logger.info(
        "Sampling dates updated; the {} dates now range from {} to {}".format(
            len(date_list), date_list[0], date_list[-1]))


def validate_fips(raw_fips, keep_outdated=False):
    """
    Fix county FIPS code anomalies, handling illegal lengths, truncated codes
    that have lost their initial zeroes and a South Dakota county that changed
    its name and FIPS code in May 2015.
    """
    if len(raw_fips) not in [4, 5]:
        return None
    if raw_fips == '46113':  # The former Shannon County, SD
        return '46102'  # Change to 46102, Oglala Lakota County, SD
    if len(raw_fips) == 4:
        new_fips = "0{}".format(raw_fips)
    else:
        new_fips = raw_fips
    if keep_outdated is False and new_fips in IGNORE_FIPS:
        return None
    else:
        return new_fips


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
        valid_fips = validate_fips(row.get('fips'))
        sampling_date = parser.parse(row.get('date')).date()
        if valid_fips and sampling_date >= starting_date:
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
    merge_the_dades()
    update_sampling_dates()
    logger.info("Created {} CountyMortgageData objects".format(
        CountyMortgageData.objects.count()))


def validate_counties():
    for each in County.objects.all():
        each.validate()


def run(*args):  # pragma: no cover
    starting_year = MortgageDataConstant.objects.get(
        name='starting_year').value
    starting_date = datetime.date(starting_year, 1, 1)
    if args:
        load_values(s3_filename=args[0], starting_date=starting_date)
        logger.info("County mortgage data loaded; now validating counties.")
        validate_counties()
        total = County.objects.count()
        valid = County.objects.filter(valid=True).count()
        if total != 0:
            logger.info(
                "{} counties of {} were found to be valid -- {}%)".format(
                    valid, total, round((valid * 100.0 / total), 1)))
    else:
        logger.info('You must provide an S3 filename to load.')
