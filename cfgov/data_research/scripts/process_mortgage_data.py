import csv
import datetime
import logging
import re
from datetime import date
from io import StringIO

from django.db import transaction

import requests
from dateutil import parser
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

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
    load_mortgage_aggregates,
)


logger = logging.getLogger(__name__)


def read_source_csv(raw_source_url: str) -> StringIO:
    response = requests.get(raw_source_url)
    response.raise_for_status()
    return StringIO(response.content.decode("utf-8"))


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


def peek_num_lines(data: StringIO) -> int:
    num_lines = sum(1 for line in data)
    data.seek(0)
    return num_lines


@transaction.atomic
def load_county_mortgage_data(
    raw_data: StringIO, starting_date: date, through_date: date
) -> int:
    """Rebuild county mortgage data table.

    Returns number of CountyMortgageData objects created.
    """
    CountyMortgageData.objects.all().delete()

    batch = []
    total_created = 0
    batch_size = 1000

    # Cache county FIPS codes.
    fips_county_pks = dict(County.objects.values_list("fips", "pk"))

    for row in tqdm(csv.DictReader(raw_data), total=peek_num_lines(raw_data)):
        sampling_date = parser.parse(row.get("date")).date()
        if sampling_date < starting_date or sampling_date > through_date:
            continue

        valid_fips = validate_fips(row.get("fips"))
        if valid_fips:
            batch.append(
                CountyMortgageData(
                    fips=valid_fips,
                    date=sampling_date,
                    total=row.get("open"),
                    current=row.get("current"),
                    thirty=row.get("thirty"),
                    sixty=row.get("sixty"),
                    ninety=row.get("ninety"),
                    other=row.get("other"),
                    county_id=fips_county_pks[valid_fips],
                )
            )

        if len(batch) >= batch_size:
            CountyMortgageData.objects.bulk_create(batch)
            total_created += len(batch)
            batch = []

    if batch:
        CountyMortgageData.objects.bulk_create(batch)
        total_created += len(batch)

    return total_created


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
    starter = datetime.datetime.now()
    starting_date = MortgageDataConstant.objects.get(
        name="starting_date"
    ).date_value

    through_date = get_thrudate(source_file)
    logger.info(f"Using through_date of {through_date}")

    source_data = read_source_csv(source_file)

    load_states()
    logger.info("States loaded")
    load_counties()
    logger.info("Counties loaded")

    logger.info("Now rebuilding the county mortgage table")
    new_objects = load_county_mortgage_data(
        source_data, starting_date=starting_date, through_date=through_date
    )
    logger.info(
        f"\nTook {datetime.datetime.now() - starter} "
        f"to create {new_objects:,} countymortgage records"
    )


def run(*args):
    """Process the latest data source and dump CSV outputs locally.

    Requires one argument, the URL of the latest source filename, which must
    match the pattern:
        delinquency_county_{MMYY}.csv
    Sample command:
        manage.py runscript process_mortgage_data \
            --script-args https://raw.github.local/org/repo/path/to/data/delinquency_county_0925.csv
    """
    if not args:
        logger.error("Pass the URL to the latest input CSV file")
        exit(1)

    process_source(args[0])
    load_mortgage_aggregates.run()
