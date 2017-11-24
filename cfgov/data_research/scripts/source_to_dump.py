from __future__ import unicode_literals

import datetime
import logging
import sys

import unicodecsv
from dateutil import parser

from data_research.models import County, MortgageDataConstant
from data_research.mortgage_utilities.fips_meta import validate_fips
from data_research.mortgage_utilities.s3_utils import (
    S3_SOURCE_BUCKET, S3_SOURCE_FILE, read_in_s3_csv
)
from data_research.mortgage_utilities.sql_utils import (
    DROP_AND_CREATE_STRING, UNLOCK_STRING, assemble_insertions
)


DEFAULT_DUMP_SLUG = '/tmp/mp_countydata'

logger = logging.getLogger(__name__)


def update_through_date_constant(date):
    constant, cr = MortgageDataConstant.objects.get_or_create(
        name='through_date')
    constant.date_value = date
    constant.save()


def convert_row_to_sql_tuple(row):
    """
    Take an amended source CSV row:
    ['1', '01001', '2008-01-01', '268', '260', '4', '1', '0', '3', '2891']

    and turn it into an SQL load tuple:
    "(1,'01001','2008-01-01',268,260,4,1,0,3,2891)"
    """
    return "({},'{}','{}',{},{},{},{},{},{},{})".format(*row)


def dump_as_csv(rows_out, dump_slug):
    """
    Drops a headerless CSV to `/tmp/mp_countydata.csv

    Sample output row:
    1,01001,2008-01-01,268,260,4,1,0,3,2891
    """
    with open('{}.csv'.format(dump_slug), 'w') as f:
        writer = unicodecsv.writer(f)
        for row in rows_out:
            writer.writerow(row)


def dump_as_sql(rows_out, dump_slug):
    """
    Drops an SQL dump file to /tmp/mp_countydata.sql

    Sample output entry:
    (1,'01001','2008-01-01',464,443,10,5,4,2,2891)
    """
    sql_rows = [convert_row_to_sql_tuple(row) for row in rows_out]

    with open('{}.sql'.format(dump_slug), 'w') as f:
        f.write(
            DROP_AND_CREATE_STRING +
            assemble_insertions(sql_rows) +
            UNLOCK_STRING.format(datetime.datetime.now()))


def create_dump(
        starting_date, through_date, dump_slug, sql=True):
    """
    Sample input CSV field_names and row:
    date,fips,open,current,thirty,sixty,ninety,other
    01/01/08,1001,268,260,4,1,0,3

    Default is to dump SQL for mysql loading. Alternative is to dump CSV.
    CSV is portable and less brittle, but our mysql setup doesn't allow it.
    If we switch to Postgres, we can make CSV the default.
    """

    starter = datetime.datetime.now()
    counter = 0
    pk = 1
    rows_out = []
    source_url = "{}/{}".format(S3_SOURCE_BUCKET, S3_SOURCE_FILE)
    raw_data = read_in_s3_csv(source_url)
    for row in raw_data:
        sampling_date = parser.parse(row.get('date')).date()
        if sampling_date >= starting_date and sampling_date <= through_date:
            valid_fips = validate_fips(row.get('fips'))
            if valid_fips:
                county_pk = County.objects.get(fips=valid_fips).pk
                rows_out.append([
                    pk,
                    valid_fips,
                    "{}".format(sampling_date),
                    row.get('open'),
                    row.get('current'),
                    row.get('thirty'),
                    row.get('sixty'),
                    row.get('ninety'),
                    row.get('other'),
                    county_pk])
                pk += 1
                counter += 1
                if counter % 10000 == 0:  # pragma: no cover
                    sys.stdout.write('.')
                    sys.stdout.flush()
                if counter % 100000 == 0:  # pragma: no cover
                    logger.info("\n{}".format(counter))
    if sql is True:
        dump_as_sql(rows_out, dump_slug)
    else:
        dump_as_csv(rows_out, dump_slug)
    logger.info('\nceate_dump took {} to create a file with {} rows'.format(
        (datetime.datetime.now() - starter), len(rows_out)))


def run(*args):
    """
    Ingests a through-date (YYYY-MM-DD) and dump location/slug. Sample command:
    `manage.py runscript source_to_dump --script-args 2017-03-01 /tmp/mp_countydata`  # noqa: E501
    Note that the script will add a `.csv` or `.sql` extension as appropriate.

    Adding an optional third arg 'csv' will dump a CSV instead of SQL:
    `--script-args 2017-03-01 /tmp/mp_countydata csv`
    """
    dump_slug = DEFAULT_DUMP_SLUG
    sql = True
    starting_date = MortgageDataConstant.objects.get(
        name='starting_date').date_value
    if args:
        through_date = parser.parse(args[0]).date()
        update_through_date_constant(through_date)
        if len(args) > 1 and args[1] != 'csv':
            dump_slug = args[1]
        if 'csv' in args:
            sql = False
        create_dump(
            starting_date, through_date, dump_slug=dump_slug, sql=sql)
    else:
        logger.info("Please provide a through-date (YYYY-MM-DD) and "
                    "a dump location/slug, such as '/tmp/mp_countydata'")
