from __future__ import unicode_literals

import json
import logging

from data_research.mortgage_utilities.fips_meta import (
    FIPS,
    FIPS_DATA_PATH,
    load_fips_meta)

from data_research.models import (
    CountyMortgageData,
    MSAMortgageData,
    NonMSAMortgageData,
    StateMortgageData)

logger = logging.getLogger(__name__)


def validate_geo(geo, fips, year, count):
    """
    A utility to check whether a county, MSA or state had an average
    monthly mortgage count in our reference year to qualify for being
    included in visualizations.
    """
    # from data_research.models import (
    #     CountyMortgageData, MSAMortgageData, StateMortgageData)
    data_objects = {
        'county': CountyMortgageData,
        'msa': MSAMortgageData,
        'state': StateMortgageData,
        'non_msa': NonMSAMortgageData
    }
    records = data_objects[geo].objects.filter(date__year=year, fips=fips)
    msum = sum([record.total for record in records if record.total])
    if records.count() != 0:
        avg = round((msum * 1.0) / records.count())
    else:
        avg = 0
    if avg > count:
        return True
    else:
        return False


def update_valid_geos():
    """
    For counties, metro areas and states, we need to include them
    in visualizations only if they meet our threshold.

    The threshold (initially 1K mortgages a month) is applied to the area's
    average for the threshold year, which is generally the previous year.

    This should be run once a year to rebuild the list of valid FIPS codes
    for visualizations. The list will be saved in the cfgov-refresh repo
    at `data_research/data/fips_whitelist.json` and can be consulted at
    runtime at FIPS.whitelist`
    """
    load_fips_meta()  # this loads the FIPS metadata object
    county_list = []
    msa_list = []
    non_msa_list = []
    state_list = []
    for fips in FIPS.county_fips:
        if validate_geo(
                'county',
                fips,
                FIPS.threshold_year,
                FIPS.threshold_count):
            county_list.append(fips)
    for fips in FIPS.msa_fips:
        if validate_geo(
                'msa',
                fips,
                FIPS.threshold_year,
                FIPS.threshold_count):
            msa_list.append(fips)
    for fips in FIPS.state_fips:
        if validate_geo(
                'state',
                fips,
                FIPS.threshold_year,
                FIPS.threshold_count):
            state_list.append(fips)
    for fips in FIPS.state_fips:
        if validate_geo(
                'non_msa',
                '{}-non'.format(fips),
                FIPS.threshold_year,
                FIPS.threshold_count):
            non_msa_list.append('{}-non'.format(fips))
    final_list = (
        sorted(county_list)
        + sorted(msa_list)
        + sorted(state_list)
        + sorted(non_msa_list))
    with open('{}/fips_whitelist.json'.format(FIPS_DATA_PATH), 'wb') as f:
        f.write(json.dumps(final_list))
    for cls in (
            CountyMortgageData,
            MSAMortgageData,
            NonMSAMortgageData,
            StateMortgageData):
        for record in cls.objects.filter(fips__in=final_list):
            record.valid = True
            if cls != CountyMortgageData:
                record.save(aggregate=False)
            else:
                record.save()
    pct_values = {
        'counties': round(len(county_list) * 100 / len(FIPS.county_fips)),
        'msas': round(len(msa_list) * 100 / len(FIPS.msa_fips)),
        'non_msas': round(len(non_msa_list) * 100 / len(FIPS.state_fips))
    }
    message = (
        "In {}, {} percent of counties, {} percent of MSAs, and {} percent of "
        "non-MSAs met our mortgage-count threshold for visualizations.".format(
            FIPS.threshold_year,
            pct_values['counties'],
            pct_values['msas'],
            pct_values['non_msas']))
    logger.info(message)


def run():  # pragma: no cover
    update_valid_geos()
