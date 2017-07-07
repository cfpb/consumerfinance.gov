from __future__ import unicode_literals
from dateutil import parser

from data_research.models import (
    # CountyMortgageData,
    MSAMortgageData,
    # StateMortgageData,
    # USMortgageData,
)
from data_research.views import (
    FIPS,
    load_fips_meta,
)
"""
sample values for FIPS.msa_fips dict:
{'46140':
    {'fips': '46140',
     'msa': 'Tulsa, OK',
     'county_list': [
        '40037', '40111', '40113', '40117', '40131', '40143', '40145']
    }
}
"""


def load_msa_values(date):
    """
    This routine should follow a refresh of county mortgage data.

    MSA values are updated by cycling through all sampling dates
    and creating or updating an MSA data object for each date.
    Saving the MSA object populates its values by aggregating data
    from all of its included counties.


    """
    created = 0
    updated = 0
    for msa_fips in FIPS.msa_fips.keys():
        _map = FIPS.msa_fips[msa_fips]
        msa_obj, cr = MSAMortgageData.objects.get_or_create(
            date=parser.parse(date).date(),
            fips=msa_fips)
        if cr:
            created += 1
        else:
            updated += 1
        county_string = ", ".join(_map['county_list'])
        if msa_obj.counties != county_string:
            msa_obj.counties = ", ".join(_map['county_list'])
            msa_obj.save()  # saving populates the object with aggregated data
    print("Created {} MSA objects and updated {} for {}".format(
        created, updated, date))


def run():
    load_fips_meta()
    for date in FIPS.dates:
        load_msa_values(date)
