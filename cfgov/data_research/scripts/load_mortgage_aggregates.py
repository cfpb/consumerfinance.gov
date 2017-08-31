from __future__ import unicode_literals

from dateutil import parser
import logging

from data_research.models import (
    MetroArea, MSAMortgageData,
    NationalMortgageData,
    # MortgageMetaData,
    NonMSAMortgageData,
    State, StateMortgageData
)
from data_research.mortgage_utilities.fips_meta import FIPS, load_fips_meta

logger = logging.getLogger(__name__)


def load_msa_values(date):
    for metro in MetroArea.objects.all():
        msa_obj, cr = MSAMortgageData.objects.get_or_create(
            date=parser.parse(date).date(),
            msa=metro,
            fips=metro.fips)
        msa_obj.aggregate_data()


def load_state_values(date):
    for state in State.objects.all():
        record, cr = StateMortgageData.objects.get_or_create(
            date=parser.parse(date).date(),
            state=state,
            fips=state.fips)
        record.aggregate_data()


def load_non_msa_state_values(date):
    for state in State.objects.all():
        record, cr = NonMSAMortgageData.objects.get_or_create(
            date=parser.parse(date).date(),
            state=state,
            fips='{}-non'.format(state.fips))
        record.aggregate_data()


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
