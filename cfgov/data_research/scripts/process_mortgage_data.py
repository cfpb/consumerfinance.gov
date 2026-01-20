import csv
import logging
import os
import re
from datetime import date, datetime
from io import StringIO

import requests
from dateutil.relativedelta import relativedelta

from data_research.models import (
    County,
    CountyMortgageData,
    MortgageDataConstant,
)
from data_research.mortgage_utilities.fips_meta import (
    load_counties,
    load_metros,
    load_states,
    update_geo_meta,
    validate_fips,
)
from data_research.scripts import (
    export_public_csvs,
    load_mortgage_aggregates,
    update_county_msa_meta,
)


SCRIPT_NAME = os.path.basename(__file__).split(".")[0]
logger = logging.getLogger(__name__)


def read_source_csv(raw_source_url: str) -> csv.DictReader:
    response = requests.get(raw_source_url)
    response.raise_for_status()
    f = StringIO(response.content.decode("utf-8"))
    return csv.DictReader(f)


def get_thrudate(filename: str) -> date:
    """Use the latest filename to derive a through_date for processing.

    The source file ends with a MMYY date suffix that we can use.
    A typical source file name: delinquency_county_0625.csv
    We exclude the latest 3 months of data because the most recent
    reports are incomplete and can show misleading results. For that reason,
    the thru_date year needs to be pushed back a year for 03 data.
    """
    match = re.search(r"_(03|06|09|12)(\d{2})\.csv$", filename)
    if not match:
        raise ValueError(
            "Filename must match *_MMYY.csv, where MM is 03, 06, 09, or 12"
        )

    month = int(match.group(1))
    year = (date.today().year // 100) * 100 + int(match.group(2))
    return date(year, month, 1) - relativedelta(months=3)


def process_source(source_file):
    """
    Re-generate aggregated data from the latest source CSV posted to S3.

    This operation has four main steps:
    - Wipe and regenerate the base county_mortgage_data table.
    - Regenerate aggregated data for MSAs, non-MSAs, states and national.
    - Update metadata values and files.
    - Export 6 downloadable public CSV files to s3 and update CSV metadata.

    The input filename should have this form: delinquency_county_{MMYY}.csv
    Expected quarterly month values are 03, 06, 09, and 12.
    The input CSV has the following field_names and row form:

    date,fips,open,current,thirty,sixty,ninety,other
    01/01/08,1001,268,260,4,1,0,3
    """
    starter = datetime.now()
    starting_date = MortgageDataConstant.objects.get(
        name="starting_date"
    ).date_value

    through_date = get_thrudate(source_file)
    logger.info(f"Using through_date of {through_date}")

    raw_data = read_source_csv(source_file)
    counter = 0
    pk = 1
    new_objects = []

    load_states()
    logger.info("States loaded")
    load_counties()
    update_geo_meta("county")
    logger.info("Counties loaded")
    load_metros()
    update_geo_meta("metro")
    logger.info("Metros loaded \nNow loading county mortgage data")
    CountyMortgageData.objects.all().delete()
    for row in raw_data:
        sampling_date = datetime.strptime(row.get("date"), "%m/%d/%y").date()
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
                if counter % 100000 == 0:  # pragma: no cover
                    logger.info(f"{counter:,}")
    CountyMortgageData.objects.bulk_create(new_objects)
    logger.info(
        f"\n{SCRIPT_NAME} took {datetime.now() - starter} "
        f"to create {len(new_objects):,} CountyMortgageData records"
    )


def run(*args):
    """Process the latest data source and dump CSV outputs locally.

    Requires one argument, the URL of the latest source filename,
    which must match the pattern delinquency_county_{MMYY}.csv.

    Sample command:
        manage.py runscript process_mortgage_data \
            --script-args https://raw.github.local/org/repo/path/to/data/delinquency_county_0925.csv

    This script will fetch input data, populate the database, and export
    public CSVs. The LOCAL_MORTGAGE_FILEPATH environment variable can be
    used to dump public CSVs locally instead of to S3.
    """
    if not args:
        logger.error("Pass the URL to the latest input CSV file")
        exit(1)

    process_source(args[0])
    load_mortgage_aggregates.run()
    update_county_msa_meta.run()
    export_public_csvs.run()
