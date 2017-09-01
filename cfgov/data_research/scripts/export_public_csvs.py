from __future__ import unicode_literals

import datetime
from dateutil import parser
from cStringIO import StringIO
import logging

import unicodecsv

from core.utils import format_file_size
from data_research.models import (
    CountyMortgageData,
    MSAMortgageData,
    MortgageMetaData,
    NationalMortgageData,
    StateMortgageData,
)
from data_research.mortgage_utilities.s3_utils import (
    bake_csv_to_s3, MORTGAGE_SUB_BUCKET, S3_MORTGAGE_DOWNLOADS_BASE)
from data_research.mortgage_utilities.fips_meta import FIPS, load_fips_meta

BASE_DATE = datetime.date(2008, 1, 1)
BASE_QUERYSET = CountyMortgageData.objects.filter(date__gte=BASE_DATE)
NATION_QUERYSET = NationalMortgageData.objects.filter(date__gte=BASE_DATE)


NATION_STARTER = {
    'RegionType': 'National',
    'State': '',
    'Name': 'United States',
    'FIPSCode': '',
    'CBSACode': ''}


LATE_VALUE_TITLE = {
    'percent_30_60': 'Percent-30-89',
    'percent_90': 'Percent-90+',
}


logger = logging.getLogger(__name__)


def save_metadata(csv_size, slug, thru_month, days_late, geo_type):
    """Save slug, URL, thru_month and file size of a new CSV download file."""
    pub_date = "{}".format(datetime.date.today())
    csv_url = "{}/{}.csv".format(S3_MORTGAGE_DOWNLOADS_BASE, slug)
    download_meta_file, cr = MortgageMetaData.objects.get_or_create(
        name='download_files')
    new_posting = {geo_type:
                   {'slug': slug,
                    'url': csv_url,
                    'size': csv_size,
                    'thru_month': thru_month,
                    'pub_date': pub_date}}
    if not download_meta_file.json_value:
        download_meta_file.json_value = {thru_month: {days_late: new_posting}}
    else:
        current = download_meta_file.json_value
        if thru_month in current:
            if days_late in current[thru_month]:
                current[thru_month][days_late].update(new_posting)
            else:
                current[thru_month].update({days_late: new_posting})
        else:
            current.update({thru_month: {days_late: new_posting}})
        download_meta_file.json_value = current
    download_meta_file.save()
    logger.info("Saved metadata for {}".format(slug))


def round_pct(value):
    return round((value * 100), 1)


def row_starter(geo_type, meta):
    if geo_type == 'County':
        return [geo_type,
                meta['state'],
                meta['name'],
                "'{}'".format(meta['fips'])]
    else:
        return [geo_type, meta['name'], "'{}'".format(meta['fips'])]


def fill_nation_row_date_values(date_set):
    """Assemble values for the repeated National row in CSV downloads."""
    FIPS.nation_row = {'percent_30_60': [], 'percent_90': []}
    for date in date_set:
        nation_obj = NATION_QUERYSET.filter(date=date).first()
        if not nation_obj:
            for key in FIPS.nation_row:
                FIPS.nation_row[key].append('')
        else:
            for key in FIPS.nation_row:
                FIPS.nation_row[key].append(
                    round_pct(getattr(nation_obj, key)))


def export_downloadable_csv(geo_type, late_value):
    """
    Export a dataset to S3 as a UTF-8 CSV file, adding single quotes
    to FIPS codes so that Excel doesn't strip leading zeros.

    geo_types are County, MetroArea or State.
    late_values are percent_30_60 or percent_90.

    Each CSV is to start with a National row for comparison.

    CSVs are posted at
    http://files.consumerfinance.gov.s3.amazonaws.com/data/mortgage-performance/downloads/  # noqa: E501

    The script also stores URLs and file sizes for use in page footnotes.
    """
    date_list = FIPS.short_dates
    thru_date = FIPS.dates[-1]
    thru_month = thru_date[:-3]
    geo_dict = {
        'County': {
            'queryset': BASE_QUERYSET,
            'headings': ['RegionType', 'State', 'Name', 'FIPSCode'],
            'meta': FIPS.county_fips
        },
        'MetroArea': {
            'queryset': MSAMortgageData.objects.filter(date__gte=BASE_DATE),
            'headings': ['RegionType', 'Name', 'CBSACode'],
            'meta': FIPS.msa_fips
        },
        'State': {
            'queryset': StateMortgageData.objects.filter(date__gte=BASE_DATE),
            'headings': ['RegionType', 'Name', 'FIPSCode'],
            'meta': FIPS.state_fips
        },
    }
    slug = "{}Mortgages{}DaysLate-thru-{}".format(
        geo_type, LATE_VALUE_TITLE[late_value], thru_month)
    _map = geo_dict.get(geo_type)
    meta = _map['meta']
    csvfile = StringIO()
    writer = unicodecsv.writer(csvfile)
    writer.writerow(_map['headings'] + date_list)
    nation_starter = [NATION_STARTER[heading]
                      for heading in _map['headings']]
    nation_ender = FIPS.nation_row[late_value]
    writer.writerow(nation_starter + nation_ender)
    for fips in sorted(meta.keys()):
        geos = _map['queryset'].filter(fips=fips)
        geo_starter = row_starter(geo_type, meta[fips])
        geo_ender = [round_pct(getattr(geo, late_value)) for geo in geos]
        writer.writerow(geo_starter + geo_ender)
    bake_csv_to_s3(
        slug,
        csvfile,
        sub_bucket="{}/downloads".format(MORTGAGE_SUB_BUCKET))
    logger.info("Baked {} to S3".format(slug))
    csvfile.seek(0, 2)
    bytecount = csvfile.tell()
    csv_size = format_file_size(bytecount)
    save_metadata(csv_size, slug, thru_month, late_value, geo_type)


def run(prep_only=False):
    load_fips_meta()
    date_set = [parser.parse(date).date() for date in FIPS.dates]
    fill_nation_row_date_values(date_set)

    if prep_only is False:
        logger.info('Exporting public CSVs to S3 ...')
        for geo in ['County', 'MetroArea', 'State']:
            export_downloadable_csv(geo, 'percent_30_60')
            logger.info('Exported 30-89-day {} CSV'.format(geo))
            export_downloadable_csv(geo, 'percent_90')
            logger.info('Exported 90-day {} CSV'.format(geo))
