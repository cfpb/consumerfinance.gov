import logging
import os
import sys

from dateutil import parser

from data_research.models import (
    County,
    CountyMortgageData,
    MortgageDataConstant,
)
from data_research.mortgage_utilities.fips_meta import validate_fips
from data_research.mortgage_utilities.s3_utils import (
    S3_SOURCE_BUCKET,
    S3_SOURCE_FILE,
    read_in_s3_csv,
)

logger = logging.getLogger(__name__)
script = os.path.basename(__file__)

# sample CSV field_names and row:
# date,fips,open,current,thirty,sixty,ninety,other
# 01/01/98,1001,268,260,4,1,0,3


def load_values(return_fips=False):
    """
    Drop and reload the CountyMortgageData table, or just return a FIPS list.

    This is not used in the data pipeline and is mainly for local testing.
    Passing `return_fips=True` will return a sorted list of source FIPS values.
    The script assumes that `starting_date` and `through_date`
    have been set in constants.
    """

    counter = 0
    source_url = "{}/{}".format(S3_SOURCE_BUCKET, S3_SOURCE_FILE)
    starting_date = MortgageDataConstant.objects.get(
        name="starting_date"
    ).date_value
    through_date = MortgageDataConstant.objects.get(
        name="through_date"
    ).date_value
    raw_data = read_in_s3_csv(source_url)
    # raw_data is a generator delivering data dicts, each representing a row
    if return_fips is True:
        fips_list = [validate_fips(row.get("fips")) for row in raw_data]
        return sorted(set(fips_list))
    logger.info("Deleting CountyMortgageData objects.")
    CountyMortgageData.objects.all().delete()
    logger.info(
        "CountyMorgtgageData count is now {}".format(
            CountyMortgageData.objects.count()
        )
    )
    for row in raw_data:
        sampling_date = parser.parse(row.get("date")).date()
        if sampling_date >= starting_date and sampling_date <= through_date:
            valid_fips = validate_fips(row.get("fips"))
            if valid_fips:
                county = County.objects.get(fips=valid_fips)
                obj = CountyMortgageData(
                    fips=valid_fips,
                    county=county,
                    date=sampling_date,
                    total=int(row.get("open")),
                    current=int(row.get("current")),
                    thirty=int(row.get("thirty")),
                    sixty=int(row.get("sixty")),
                    ninety=int(row.get("ninety")),
                    other=int(row.get("other")),
                )
                obj.save()
                counter += 1
                if counter % 10000 == 0:  # pragma: no cover
                    sys.stdout.write(".")
                    sys.stdout.flush()
                if counter % 100000 == 0:  # pragma: no cover
                    logger.info("\n{}".format(counter))
    logger.info(
        "\nCreated {} CountyMortgageData objects".format(
            CountyMortgageData.objects.count()
        )
    )


def run():  # pragma: no cover
    load_values()
