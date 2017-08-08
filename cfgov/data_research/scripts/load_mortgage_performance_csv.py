from __future__ import unicode_literals

from dateutil import parser
import sys

from data_research.models import CountyMortgageData
from data_research.mortgage_utilities.s3_utils import read_in_s3_csv
from data_research.mortgage_utilities.fips_meta import (
    SOURCE_CSV_URL, OUTDATED_FIPS
)


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


def validate_fips(raw_fips, keep_outdated=False):
    """
    Fix county FIPS code anomalies, handling illegal lengths, truncated codes
    that have lost their initial zeroes and a South Dakota county that changed
    its name and FIPS code in May 2015.
    """
    if len(raw_fips) not in [4, 5]:
        return None
    if raw_fips == '46113':  # Fix Oglala Lakota County, SD
        return OUTDATED_FIPS['46113']
    if len(raw_fips) == 4:
        new_fips = "0{}".format(raw_fips)
    else:
        new_fips = raw_fips
    if keep_outdated is False:
        if new_fips in OUTDATED_FIPS:
            return None
        else:
            return new_fips
    return new_fips


def load_values(return_fips=False):
    """Load source mortgage data into an empty CountyMortgageData table."""
    counter = 0
    raw_data = read_in_s3_csv(SOURCE_CSV_URL)
    # raw_data is a generator delivering data dicts, each representing a row
    if return_fips is True:
        fips_list = []
        for row in raw_data:
            fips_list.append(validate_fips(row.get('fips')))
        return sorted(set(fips_list))
    for row in raw_data:
        valid_fips = validate_fips(row.get('fips'))
        if valid_fips:
            obj = CountyMortgageData(
                fips=valid_fips,
                date=parser.parse(row.get('date')).date(),
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
                print("\n{}".format(counter))
    merge_the_dades()


def run():
    load_values()
