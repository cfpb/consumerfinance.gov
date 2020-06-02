import datetime
import logging
import os

from dateutil import parser

from data_research.models import (
    CountyMortgageData, MetroArea, MortgageMetaData, MSAMortgageData,
    NationalMortgageData, NonMSAMortgageData, State, StateMortgageData,
    validate_counties
)


logger = logging.getLogger(__name__)
script = os.path.basename(__file__)


def update_sampling_dates():
    """
    Update our metadata list of sampling dates.
    """
    dates = sorted(set([obj.date for obj in CountyMortgageData.objects.all()]))
    date_list = ["{}".format(date) for date in dates]
    date_list_obj, cr = MortgageMetaData.objects.get_or_create(
        name='sampling_dates')
    date_list_obj.json_value = date_list
    date_list_obj.save()
    logger.info(
        "Sampling dates updated; the {} dates now range from {} to {}".format(
            len(date_list), date_list[0], date_list[-1]))


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


def load_msa_values(date):
    for metro in MetroArea.objects.all():
        msa_obj, cr = MSAMortgageData.objects.get_or_create(
            date=date,
            msa=metro,
            fips=metro.fips)
        msa_obj.aggregate_data()


def load_state_values(date):
    for state in State.objects.all():
        record, cr = StateMortgageData.objects.get_or_create(
            date=date,
            state=state,
            fips=state.fips)
        record.aggregate_data()


def load_non_msa_state_values(date):
    for state in State.objects.all():
        record, cr = NonMSAMortgageData.objects.get_or_create(
            date=date,
            state=state,
            fips='{}-non'.format(state.fips))
        record.aggregate_data()


def load_national_values(date):
    record, cr = NationalMortgageData.objects.get_or_create(
        date=date,
        fips='-----')
    record.aggregate_data()


def run():
    """
    This script should be run following a refresh of county mortgage data.

    The script wipes national, state and metro-based aggregate records,
    creates new ones for every date in range, and then updates metadata.
    """
    starter = datetime.datetime.now()
    aggregate_classes = [
        NationalMortgageData,
        StateMortgageData,
        MSAMortgageData,
        NonMSAMortgageData]
    for cls in aggregate_classes:
        cls.objects.all().delete()
    update_sampling_dates()
    merge_the_dades()
    validate_counties()
    dates = MortgageMetaData.objects.get(name='sampling_dates').json_value
    for date_string in dates:
        date = parser.parse(date_string).date()
        logger.info(
            "Aggregating data for {}".format(date))
        load_msa_values(date)
        load_state_values(date)
        load_non_msa_state_values(date)
        load_national_values(date)
    logger.info("Validating MSAs and non-MSAs")
    for metro in MetroArea.objects.all():
        metro.validate()
    for state in State.objects.all():
        state.validate_non_msas()
    logger.info("{} took {} to run.".format(
        script, (datetime.datetime.now() - starter)))
