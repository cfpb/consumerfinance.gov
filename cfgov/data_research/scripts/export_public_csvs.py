import csv
import datetime
import logging
from io import StringIO

from dateutil import parser

from core.utils import format_file_size
from data_research.models import (
    County,
    CountyMortgageData,
    MetroArea,
    MortgageMetaData,
    MSAMortgageData,
    NationalMortgageData,
    NonMSAMortgageData,
    State,
    StateMortgageData,
)
from data_research.mortgage_utilities.fips_meta import FIPS, load_fips_meta
from data_research.mortgage_utilities.s3_utils import (
    MORTGAGE_SUB_BUCKET,
    S3_MORTGAGE_DOWNLOADS_BASE,
    bake_csv_to_s3,
)


NATION_QUERYSET = NationalMortgageData.objects.all()
STATES_TO_IGNORE = ["72"]  # Excluding Puerto Rico from project launch


NATION_STARTER = {
    "RegionType": "National",
    "State": "",
    "Name": "United States",
    "FIPSCode": "-----",
    "CBSACode": "-----",
}


LATE_VALUE_TITLE = {
    "percent_30_60": "Percent-30-89",
    "percent_90": "Percent-90-plus",
}


logger = logging.getLogger(__name__)


def save_metadata(csv_size, slug, thru_month, days_late, geo_type):
    """Save slug, URL, thru_month and file size of a new CSV download file."""
    pub_date = datetime.date.today().strftime("%B %Y")
    thru_month_formatted = parser.parse(thru_month).strftime("%B %Y")
    csv_url = "{}/{}.csv".format(S3_MORTGAGE_DOWNLOADS_BASE, slug)
    download_meta_file, cr = MortgageMetaData.objects.get_or_create(
        name="download_files"
    )
    new_posting = {geo_type: {"slug": slug, "url": csv_url, "size": csv_size}}
    if not download_meta_file.json_value:
        download_meta_file.json_value = {
            thru_month: {
                days_late: new_posting,
                "thru_month": thru_month_formatted,
                "pub_date": pub_date,
            }
        }
    else:
        current = download_meta_file.json_value
        if thru_month in current.keys():
            if days_late in current[thru_month].keys():
                current[thru_month][days_late].update(new_posting)
            else:
                current[thru_month][days_late] = new_posting
        else:
            current.update(
                {
                    thru_month: {
                        days_late: new_posting,
                        "thru_month": thru_month_formatted,
                        "pub_date": pub_date,
                    }
                }
            )
        download_meta_file.json_value = current
    download_meta_file.save()
    logger.info("Saved metadata for {}".format(slug))


def round_pct(value):
    return round((value * 100), 1)


def row_starter(geo_type, obj):
    if geo_type == "County":
        return [
            geo_type,
            obj.county.state.abbr,
            obj.county.name,
            "'{}'".format(obj.fips),
        ]
    elif geo_type == "MetroArea":
        return [geo_type, obj.msa.name, obj.fips]
    elif geo_type == "State":
        return [geo_type, obj.state.name, "'{}'".format(obj.fips)]
    else:
        return [geo_type, obj.state.name, obj.fips]


def fill_nation_row_date_values(date_set):
    """Assemble values for the repeated National row in CSV downloads."""
    FIPS.nation_row = {"percent_30_60": [], "percent_90": []}
    for date in date_set:
        nation_obj = NATION_QUERYSET.filter(date=date).first()
        if not nation_obj:
            for key in FIPS.nation_row:
                FIPS.nation_row[key].append("")
        else:
            for key in FIPS.nation_row:
                FIPS.nation_row[key].append(
                    round_pct(getattr(nation_obj, key))
                )


def export_downloadable_csv(geo_type, late_value):
    """
    Export a dataset to S3 as a UTF-8 CSV file.

    We add single quotes to FIPS codes so Excel doesn't strip leading zeros.

    geo_types are County, MetroArea or State.
    late_values are percent_30_60 or percent_90.
    Non-Metro areas are added to the MetroArea CSV.

    Each CSV is to start with a National row for comparison.

    CSVs are posted at
    https://files.consumerfinance.gov/data/mortgage-performance/downloads/

    The script also stores URLs and file sizes for use in page footnotes.
    """
    date_list = FIPS.short_dates
    thru_date = FIPS.dates[-1]
    thru_month = thru_date[:-3]
    geo_dict = {
        "County": {
            "queryset": CountyMortgageData.objects.filter(county__valid=True),
            "headings": ["RegionType", "State", "Name", "FIPSCode"],
            "fips_list": sorted(
                [county.fips for county in County.objects.filter(valid=True)]
            ),
        },
        "MetroArea": {
            "queryset": MSAMortgageData.objects.filter(msa__valid=True),
            "headings": ["RegionType", "Name", "CBSACode"],
            "fips_list": sorted(
                [metro.fips for metro in MetroArea.objects.filter(valid=True)]
            ),
        },
        "NonMetroArea": {
            "queryset": NonMSAMortgageData.objects.filter(
                state__non_msa_valid=True
            ),
            "headings": ["RegionType", "Name", "CBSACode"],
            "fips_list": sorted(
                [
                    "{}-non".format(state.fips)
                    for state in State.objects.filter(non_msa_valid=True)
                ]
            ),
        },
        "State": {
            "queryset": StateMortgageData.objects.all(),
            "headings": ["RegionType", "Name", "FIPSCode"],
            "fips_list": sorted(
                [
                    state.fips
                    for state in State.objects.exclude(
                        fips__in=STATES_TO_IGNORE
                    )
                ]
            ),
        },
    }
    slug = "{}Mortgages{}DaysLate-thru-{}".format(
        geo_type, LATE_VALUE_TITLE[late_value], thru_month
    )
    _map = geo_dict.get(geo_type)
    fips_list = _map["fips_list"]
    csvfile = StringIO()
    writer = csv.writer(csvfile)
    writer.writerow(_map["headings"] + date_list)
    nation_starter = [NATION_STARTER[heading] for heading in _map["headings"]]
    nation_ender = FIPS.nation_row[late_value]
    writer.writerow(nation_starter + nation_ender)
    for fips in fips_list:
        records = _map["queryset"].filter(fips=fips)
        record_starter = row_starter(geo_type, records.first())
        record_ender = [
            round_pct(getattr(record, late_value)) for record in records
        ]
        writer.writerow(record_starter + record_ender)
    if geo_type == "MetroArea":
        non_map = geo_dict["NonMetroArea"]
        for fips in non_map["fips_list"]:
            records = non_map["queryset"].filter(fips=fips)
            record_starter = row_starter("NonMetroArea", records.first())
            record_ender = [
                round_pct(getattr(record, late_value)) for record in records
            ]
            writer.writerow(record_starter + record_ender)
    bake_csv_to_s3(
        slug, csvfile, sub_bucket="{}/downloads".format(MORTGAGE_SUB_BUCKET)
    )
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
        logger.info("Exporting public CSVs to S3 ...")
        for geo in ["County", "MetroArea", "State"]:
            export_downloadable_csv(geo, "percent_30_60")
            logger.info("Exported 30-89-day {} CSV".format(geo))
            export_downloadable_csv(geo, "percent_90")
            logger.info("Exported 90-day {} CSV".format(geo))
