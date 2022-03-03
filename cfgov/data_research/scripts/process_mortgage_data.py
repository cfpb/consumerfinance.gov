import csv
import datetime
import logging
import os
import sys
from io import StringIO

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
from data_research.scripts import (
    export_public_csvs,
    load_mortgage_aggregates,
    update_county_msa_meta,
)

DEFAULT_DUMP_SLUG = "/tmp/mp_countydata"
DATAFILE = StringIO()
SCRIPT_NAME = os.path.basename(__file__).split(".")[0]
logger = logging.getLogger(__name__)


def update_through_date_constant(date):
    constant, cr = MortgageDataConstant.objects.get_or_create(
        name="through_date"
    )
    constant.date_value = date
    constant.save()


def dump_as_csv(rows_out, dump_slug):
    """
    Drops a headerless CSV to `/tmp/mp_countydata.csv

    Sample output row:
    1,01001,2008-01-01,268,260,4,1,0,3,2891
    """
    with open("{}.csv".format(dump_slug), "w") as f:
        writer = csv.writer(f)
        for row in rows_out:
            writer.writerow(row)


def process_source(starting_date, through_date, dump_slug=None):
    """
    Re-generate aggregated data from the latest source CSV posted to S3.

    This operation has three steps
    - Wipe and regenerate the base county_mortgage_data table.
    - Regenerate aggregated data for MSAs, non-MSAs, states and national.
    - Update metadata values and files.
    - Export new downloadable public CSV files.

    If dump_slug is provided, a CSV the base county tables will be dumped.

    The input CSV has the following field_names and row form:
    date,fips,open,current,thirty,sixty,ninety,other
    01/01/08,1001,268,260,4,1,0,3

    """
    starter = datetime.datetime.now()
    counter = 0
    pk = 1
    new_objects = []
    # truncate table
    CountyMortgageData.objects.all().delete()
    source_url = "{}/{}".format(S3_SOURCE_BUCKET, S3_SOURCE_FILE)
    raw_data = read_in_s3_csv(source_url)
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
                    logger.info("\n{}".format(counter))
    CountyMortgageData.objects.bulk_create(new_objects)
    logger.info(
        "\n{} took {} "
        "to create {} countymortgage records".format(
            SCRIPT_NAME, (datetime.datetime.now() - starter), len(new_objects)
        )
    )
    if dump_slug:
        dump_as_csv(
            (
                (
                    obj.pk,
                    obj.fips,
                    "{}".format(obj.date),
                    obj.total,
                    obj.current,
                    obj.thirty,
                    obj.sixty,
                    obj.ninety,
                    obj.other,
                    obj.county.pk,
                )
                for obj in new_objects
            ),
            dump_slug,
        )


def run(*args):
    """
    Proces latest data source and optionally drop a CSV of result.

    The script ingests a through-date (YYYY-MM-DD) and dump location/slug.
    Sample command:
    `manage.py runscript process_mortgage_data --script-args 2017-03-01 /tmp/mp_countydata`  # noqa: B950
    """
    dump_slug = None
    starting_date = MortgageDataConstant.objects.get(
        name="starting_date"
    ).date_value
    if args:
        through_date = parser.parse(args[0]).date()
        update_through_date_constant(through_date)
        if len(args) > 1:
            dump_slug = args[1]
        process_source(starting_date, through_date, dump_slug=dump_slug)
        load_mortgage_aggregates.run()
        update_county_msa_meta.run()
        export_public_csvs.run()
    else:
        logger.info(
            "Please provide a through-date (YYYY-MM-DD).\n"
            "Optionally, you may also provide a dump location/slug, "
            "such as '/tmp/mp_countydata.csv', if you want a CSV dumped.\n"
        )
