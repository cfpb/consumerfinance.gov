import csv
import datetime
import logging
import os
import sys
from io import StringIO

import requests
from dateutil import parser

from data_research.models import (
    County,
    CountyMortgageData,
    MortgageDataConstant,
)
from data_research.mortgage_utilities.fips_meta import (
    load_counties,
    load_states,
    validate_fips,
)
from data_research.scripts import (
    export_public_csvs,
    load_mortgage_aggregates,
    thrudate,
    update_county_msa_meta,
)


MORTGAGE_PERFORMANCE_SOURCE = os.getenv("MORTGAGE_PERFORMANCE_SOURCE")
DATAFILE = StringIO()
SCRIPT_NAME = os.path.basename(__file__).split(".")[0]
logger = logging.getLogger(__name__)


def update_through_date_constant(date):
    constant, cr = MortgageDataConstant.objects.get_or_create(
        name="through_date"
    )
    constant.date_value = date
    constant.save()


def read_source_csv(source_file):
    raw_source_url = f"{MORTGAGE_PERFORMANCE_SOURCE}/{source_file}"
    response = requests.get(raw_source_url)
    f = StringIO(response.content.decode("utf-8"))
    reader = csv.DictReader(f)
    return reader


def process_source(source_file):
    """
    Re-generate aggregated data from the latest source CSV posted to S3.

    This operation has four main steps:
    - Wipe and regenerate the base county_mortgage_data table.
    - Regenerate aggregated data for MSAs, non-MSAs, states and national.
    - Update metadata values and files.
    - Export new downloadable public CSV files to s3, or dump them locally.

    To dump the six CSV downloads locally, add this env var before starting,
    and specify a local path for the files; develop-apps is just an example:
    export LOCAL_MORTGAGE_FILEPATH=develop-apps

    The input filename should have this form: delinquency_county_{MMYY}.csv
    Expected quarterly month values are 03, 06, 09, and 12.
    The input CSV has the following field_names and row form:

    date,fips,open,current,thirty,sixty,ninety,other
    01/01/08,1001,268,260,4,1,0,3
    """
    starter = datetime.datetime.now()
    starting_date = MortgageDataConstant.objects.get(
        name="starting_date"
    ).date_value
    thru_date_string = thrudate.get_thrudate(source_file)
    logger.info(f"Using through_date of {thru_date_string}")
    through_date = parser.parse(thru_date_string).date()
    update_through_date_constant(through_date)
    raw_data = read_source_csv(source_file)
    counter = 0
    pk = 1
    new_objects = []

    load_states()
    logger.info("States loaded")
    load_counties()
    logger.info("Counties loaded")
    logger.info("Now rebuilding the county mortgage table")
    CountyMortgageData.objects.all().delete()
    for row in raw_data:
        sampling_date = parser.parse(row.get("date")).date()
        if sampling_date >= starting_date and sampling_date <= through_date:
            valid_fips = validate_fips(row.get("fips"))
            if valid_fips:
                county = County.objects.get(fips=valid_fips)
                new_objects.append(
                    CountyMortgageData(
                        pk=pk,
                        fips=valid_fips,
                        date=sampling_date,
                        total=row.get("open"),
                        current=row.get("current"),
                        thirty=row.get("thirty"),
                        sixty=row.get("sixty"),
                        ninety=row.get("ninety"),
                        other=row.get("other"),
                        county=county,
                    )
                )
                pk += 1
                counter += 1
                if counter % 10000 == 0:  # pragma: no cover
                    sys.stdout.write(".")
                    sys.stdout.flush()
                if counter % 100000 == 0:  # pragma: no cover
                    logger.info(f"\n{counter}:,")
    CountyMortgageData.objects.bulk_create(new_objects)
    logger.info(
        f"\n{SCRIPT_NAME} took {datetime.datetime.now() - starter} "
        f"to create {len(new_objects):,} countymortgage records"
    )


def run(*args):
    """
    Process the latest data source and optionally dump CSV downloads locally.

    You must pass a source filename in the form delinquency_county_{MMYY}.csv
    Sample command:
        manage.py runscript process_mortgage_data \
            --script-args delinquency_county_0625.csv

    Local downloads can be triggered by an env var specifying a location:
    Example: `export LOCAL_MORTGAGE_FILEPATH=develop-apps`
    That will dump the six export CSVs locally instead of pushing them to s3.
    """
    if not args:
        logger.error(
            "Pass a source file with the form 'delinquency_county_{MMYY}.csv'"
        )
        return
    if not MORTGAGE_PERFORMANCE_SOURCE:
        logger.error(
            "Processing requires a MORTGAGE_PERFORMANCE_SOURCE env value."
        )
        return
    arg = args[0]
    if arg == "export-csvs-only":
        export_public_csvs.run()
    else:
        source_file = arg
        process_source(source_file)
        load_mortgage_aggregates.run()
        update_county_msa_meta.run()
        export_public_csvs.run()
