from __future__ import unicode_literals

from dateutil import parser
import logging

from data_research.models import (
    MSAMortgageData,
    NationalMortgageData,
    NonMSAMortgageData,
    StateMortgageData,
)
from data_research.views import FIPS, load_fips_meta

logger = logging.getLogger(__name__)


def load_msa_values(date):
    for msa_fips in FIPS.msa_fips:
        _map = FIPS.msa_fips[msa_fips]
        msa_obj, cr = MSAMortgageData.objects.get_or_create(
            date=parser.parse(date).date(),
            fips=msa_fips)
        if cr:
            FIPS.created += 1
        else:
            FIPS.updated += 1
        county_string = ", ".join(_map['county_list'])
        if msa_obj.counties != county_string:
            msa_obj.counties = county_string
            if msa_obj.counties:
                msa_obj.save()


def load_state_values(date):
    for state_fips in FIPS.state_fips.keys():
        record, cr = StateMortgageData.objects.get_or_create(
            date=parser.parse(date).date(),
            fips=state_fips)
        if cr:
            FIPS.created += 1
        else:
            FIPS.updated += 1
        record.save()


def load_non_msa_state_values(date):
    for state_fips in FIPS.state_fips.keys():
        record, cr = NonMSAMortgageData.objects.get_or_create(
            date=parser.parse(date).date(),
            fips='{}-non'.format(state_fips))
        if cr:
            FIPS.created += 1
        else:
            FIPS.updated += 1
        record.save()


def load_national_values(date):
    record, cr = NationalMortgageData.objects.get_or_create(
        date=parser.parse(date).date(),
        fips='-----')
    record.save()
    if cr:
        FIPS.created += 1
    else:
        FIPS.updated += 1


def run():
    """
    This script should be run following a refresh of county mortgage data.

    The script makes sure a national, state or metro aggregate record exists
    for every relevant date, then saves the record, which triggers aggregation
    calculations. Resulting aggregate values are stored in the record.
    """
    load_fips_meta()
    for date in FIPS.dates:
        logger.info(
            "aggregating data for {}".format(date))
        load_msa_values(date)
        load_state_values(date)
        load_non_msa_state_values(date)
        load_national_values(date)
    logger.info("Created {} records and updated {}".format(
        FIPS.created, FIPS.updated))
