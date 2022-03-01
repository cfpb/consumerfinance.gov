import datetime
import json
import os
import zipfile
from collections import OrderedDict
from csv import DictReader as cdr, writer as csw
from pathlib import Path
from subprocess import call

from django.contrib.humanize.templatetags.humanize import intcomma

import requests

from paying_for_college.models import Alias, School
from paying_for_college.views import get_school


SCRIPT = os.path.basename(__file__).partition(".")[0]
PFC_ROOT = Path(__file__).resolve().parents[2]

# DATA_YEAR specifies first year of an academic-year pair.
# Normally we'd run this script early in a calendar year, which will be
# in the middle of an academic year. So the latest data available will be
# from the previous academic year, whose first year is two years ago.
# In early 2020, the latest data came from the 2018-2019 academic year.
DATA_YEAR = datetime.datetime.now().year - 2
ipeds_directory = "{}/data_sources/ipeds".format(PFC_ROOT)
ipeds_data_url = "http://nces.ed.gov/ipeds/datacenter/data"
data_slug = "IC{}_AY".format(DATA_YEAR)
dictionary_slug = "IC{}_AY_Dict".format(DATA_YEAR)

DATA_VARS = {
    "universe_url": "{}/HD{}.zip".format(ipeds_data_url, DATA_YEAR),
    "universe_zip": "{}/HD{}.zip".format(ipeds_directory, DATA_YEAR),
    "universe_csv": "{}/hd{}.csv".format(ipeds_directory, DATA_YEAR),
    "universe_cleaned": "{}/hd{}_cleaned.csv".format(
        ipeds_directory, DATA_YEAR
    ),
    "data_url": "{}/{}.zip".format(ipeds_data_url, data_slug),
    "data_zip": "{}/{}.zip".format(ipeds_directory, data_slug),
    "data_csv": "{}/{}.csv".format(ipeds_directory, data_slug.lower()),
    "data_cleaned": "{}/{}_cleaned.csv".format(
        ipeds_directory, data_slug.lower()
    ),
    "services_url": "{}/IC{}.zip".format(ipeds_data_url, DATA_YEAR),
    "services_zip": "{}/IC{}.zip".format(ipeds_directory, DATA_YEAR),
    "services_csv": "{}/ic{}.csv".format(ipeds_directory, DATA_YEAR),
    "services_cleaned": "{}/ic{}_cleaned.csv".format(
        ipeds_directory, DATA_YEAR
    ),
}

# mapping the vars of our data_json to the IPEDS data csv
# We pull only one value, 'ROOM', from the IPEDS services csv
DATA_POINTS = {
    "books": "CHG4AY3",
    "otherOffCampus": "CHG8AY3",
    "otherOnCampus": "CHG6AY3",
    "otherWFamily": "CHG9AY3",
    "roomBrdOffCampus": "CHG7AY3",
    "roomBrdOnCampus": "CHG5AY3",
    "tuitionGradInDis": "TUITION5",
    "tuitionGradInS": "TUITION6",
    "tuitionGradOss": "TUITION7",
    "tuitionUnderInDis": "TUITION1",
}

KEYS = sorted([key.upper() for key in DATA_POINTS] + ["ROOM"])
STARTER_DICT = OrderedDict()
for key in KEYS:
    STARTER_DICT[key] = None
STARTER_DATA_JSON = json.dumps(STARTER_DICT)

NEW_SCHOOL_DATA_POINTS = {
    "alias": "INSTNM",
    "city": "CITY",
    "state": "STABBR",
    "zip5": "ZIP",
    "url": "WEBADDR",
    "degrees_highest": "HLOFFER",
    "operating": "CYACTIVE",
}

# other columns of possible interest in the 'universe' spreadsheet:
# NEWID: the UNITID for merged schools
# DEATHYR: Year institution was deleted from IPEDS
# CLOSEDAT: Date institution closed


def icomma(value):
    return intcomma(value, use_l10n=False)


def unzip_file(filepath):
    """Unzip a .zip file and store contents in the ipeds directory."""
    zip_ref = zipfile.ZipFile(filepath, "r")
    zip_ref.extractall(ipeds_directory)
    zip_ref.close()
    return True


def download_zip_file(url, zip_file):
    """Download a .zip file, unzip it, and then delete the .zip file."""
    resp = requests.get(url, stream=True)
    if resp.ok:
        with open(zip_file, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        unzip_file(zip_file)
        call(["rm", zip_file])
        return True
    else:
        return False


def write_clean_csv(fpath, fieldnames, clean_headings, data):
    with open(fpath, "w") as f:
        writer = csw(f)
        writer.writerow(clean_headings)
        for row in data:
            writer.writerow([row[name] for name in fieldnames])


def download_files():
    """Download the latest IPEDS Institutional Characteristics file."""
    for slug in ["universe", "data", "services"]:
        url = DATA_VARS["{}_url".format(slug)]
        target = DATA_VARS["{}_zip".format(slug)]
        target_slug = target.split("/")[-1]
        if download_zip_file(url, target):
            print("Downloaded {}".format(target_slug))
        else:
            print("Failed to download {}".format(target_slug))
    clean_csv_headings()


def read_csv(fpath, encoding="utf-8"):
    if not os.path.isfile(fpath):
        download_files()
    with open(fpath, newline="", encoding=encoding) as f:
        reader = cdr(f)
        data = [row for row in reader]
        return reader.fieldnames, data


def dump_csv(fpath, header, data):
    with open(fpath, "w") as f:
        writer = csw(f)
        writer.writerow(header)
        for row in data:
            writer.writerow([row[heading] for heading in header])


def clean_csv_headings():
    """Strip nasty leading or trailing spaces from column headings."""
    for slug in ["universe", "data", "services"]:
        original_file = DATA_VARS["{}_csv".format(slug)]
        cleaned_file = DATA_VARS["{}_cleaned".format(slug)]
        fieldnames, data = read_csv(original_file, encoding="latin-1")
        clean_headings = [name.strip() for name in fieldnames]
        write_clean_csv(cleaned_file, fieldnames, clean_headings, data)


def process_datafiles(add_schools=[]):
    """Collect data points from IPEDS csvs and deliver them as a dict."""
    collector = {}
    if add_schools:  # we have a list of school IDs to add to our database
        names, data = read_csv(DATA_VARS["universe_cleaned"])
        for row in data:
            _id = row["UNITID"]
            if _id in add_schools:
                collector[_id] = {}
                for key in NEW_SCHOOL_DATA_POINTS:
                    collector[_id][key] = row[NEW_SCHOOL_DATA_POINTS[key]]
        return collector
    snames, service_data = read_csv(DATA_VARS["services_cleaned"])
    for row in service_data:
        collector[row["UNITID"]] = {"onCampusAvail": row["ROOM"]}
    dnames, data = read_csv(DATA_VARS["data_cleaned"])
    for row in data:
        for key in DATA_POINTS:
            collector[row["UNITID"]][key] = row[DATA_POINTS[key]]
    return collector


def create_alias(alias, school):
    alias = Alias(alias=alias, institution=school, is_primary=True)
    alias.save()


def create_school(iped, data):
    school = School(school_id=iped, data_json=STARTER_DATA_JSON)
    for field in data:
        setattr(school, field, data[field])
    school.zip5 = school.zip5[:5]
    school.save()
    _alias = data.get("alias")
    if _alias:
        create_alias(_alias, school)


def process_missing(missing_ids):
    """Create missing school and alias objects and dump csv of additions."""
    csv_out_data = []
    csv_slug = "{}/schools_added_on_{}.csv".format(
        ipeds_directory, datetime.date.today()
    )
    missing_data = process_datafiles(add_schools=missing_ids)
    for school_id in missing_data:
        create_school(int(school_id), missing_data[school_id])
        data_row = missing_data[school_id]
        data_row["ID"] = school_id
        csv_out_data.append(data_row)
    header = sorted(csv_out_data[0].keys())
    dump_csv(csv_slug, header, csv_out_data)


def load_values(dry_run=True):
    updated = 0
    points = 0
    oncampus = 0
    source_dict = process_datafiles()
    current_ids = [school.pk for school in School.objects.all()]
    missing = [pk for pk in source_dict.keys() if int(pk) not in current_ids]
    if missing and dry_run is False:
        process_missing(missing)
    for ID in source_dict:
        new_data = source_dict[ID]
        if "onCampusAvail" in new_data:
            if new_data["onCampusAvail"] == "1":
                new_data["onCampusAvail"] = "Yes"
                oncampus += 1
            else:
                new_data["onCampusAvail"] = "No"
        school = get_school(ID)
        if school:
            school_data = STARTER_DICT
            for data_key in new_data:
                val = new_data[data_key]
                if val == ".":
                    val = None
                school_data[data_key.upper()] = val
                points += 1
            school.data_json = json.dumps(school_data)
            if not dry_run:
                school.save()
            updated += 1
    if dry_run:
        msg = (
            "DRY RUN:\n"
            "- {} would have updated {} data points for {} schools\n"
            "- {} schools found with on-campus housing\n"
            "- {} new school records "
            "would have been created".format(
                SCRIPT,
                icomma(points),
                icomma(updated),
                icomma(oncampus),
                len(missing),
            )
        )
        return msg
    msg = (
        "{} updated {} data points for {} schools;\n"
        "{} new school records were created".format(
            SCRIPT, icomma(points), icomma(updated), len(missing)
        )
    )
    return msg
