"""
Update college data using the Dept. of Education's College Scorecard API.

Scorecard documentation: https://collegescorecard.ed.gov/data/documentation/
"""
import datetime
import logging
import os
import sys
import time
from decimal import Decimal

import requests
from requests.exceptions import SSLError

from paying_for_college.disclosures.scripts import api_utils
from paying_for_college.disclosures.scripts.api_utils import (
    DECIMAL_MAP,
    MODEL_MAP,
)
from paying_for_college.models import (
    CONTROL_MAP,
    FAKE_SCHOOL_PKS,
    OFFICE_IDS,
    PROGRAM_LEVELS,
    Program,
    School,
)


logger = logging.getLogger(__name__)

DATESTAMP = datetime.datetime.now().strftime("%Y-%m-%d")
HOME = os.path.expanduser("~")
NO_DATA_FILE = "{}/no_data_{}.json".format(HOME, DATESTAMP)
SCRIPTNAME = os.path.basename(__file__).partition(".")[0]
ID_BASE = "{}?api_key={}".format(api_utils.SCHOOLS_ROOT, api_utils.API_KEY)
FIELDS = sorted(MODEL_MAP.keys())
FIELDSTRING = api_utils.build_field_string()


def test_for_program_data(program_data):
    if (
        program_data.get("earnings").get("median_earnings")
        or program_data.get("debt").get("median_debt")
        or program_data.get("debt").get("monthly_debt_payment")
    ):
        return True
    else:
        return False


def update_programs(api_data, school):
    """Create or update a school's program-level records."""
    create_count = 0
    program_data = api_data.get("latest.programs.cip_4_digit")
    for entry in program_data:
        if not test_for_program_data(entry):
            continue
        level = entry["credential"]["level"]
        cip_code = entry["code"]
        program_code = "{}-{}".format(cip_code, level)
        program, _created = Program.objects.update_or_create(
            institution=school,
            program_code=program_code,
            defaults={
                "program_name": entry["title"],
                "cip_code": cip_code,
                "completers": entry["counts"]["titleiv"],
                "level": level,
                "level_name": PROGRAM_LEVELS.get(level),
                "salary": entry["earnings"]["median_earnings"],
                "median_student_loan_completers": (
                    entry["debt"]["median_debt"]
                ),
                "median_monthly_debt": (entry["debt"]["monthly_debt_payment"]),
            },
        )
        if _created:
            create_count += 1
    return create_count


def fix_zip5(zip5):
    """Add leading zeros if they have been stripped by the scorecard db."""
    if len(zip5) == 4:
        return "0{}".format(zip5)
    if len(zip5) == 3:
        return "00{}".format(zip5)
    else:
        return zip5[:5]


def get_scorecard_data(url):
    """Make our API call to Scorecard."""
    try:
        response = requests.get(url)
    except SSLError:
        logger.exception("SSL error connecting with Scorecard")
        return
    if not response.ok:
        logger.info("request not OK, returned {}".format(response.reason))
        if response.status_code == 429:
            logger.info("API limit reached")
        return
    if not response.json() or not response.json().get("results"):
        return
    return response.json().get("results")[0]


def set_school_grad_rate(school, api_data):
    """Set the appropriate grad rate for a given school."""
    four_year_raw = api_data.get(
        "latest.completion.completion_rate_4yr_150nt_pooled"
    )
    associate_raw = api_data.get(
        "latest.completion.completion_rate_less_than_4yr_150nt_pooled"
    )
    if four_year_raw is None:
        four_year_rate = four_year_raw
    else:
        four_year_rate = Decimal(str(four_year_raw))
    if associate_raw is None:
        associate_rate = associate_raw
    else:
        associate_rate = Decimal(str(associate_raw))
    if int(school.degrees_highest) >= 3:
        school.grad_rate = four_year_rate
        school.grad_rate_4yr = four_year_rate
        school.grad_rate_lt4 = None
    else:
        school.grad_rate = associate_rate
        school.grad_rate_lt4 = associate_rate
        school.grad_rate_4yr = None
    return school


def compile_net_prices(school, api_data):
    """
    Assemble net-price and slices from new-in-2019 Scorecard endpoints.

    The former 'avg_net_price.overall' endpoint was removed in favor of
    separate values for public and private school groups.
    """
    slice_data = {}
    slice_map = {
        "latest.cost.net_price.{}.by_income_level.0-30000": "0_30k",
        "latest.cost.net_price.{}.by_income_level.30001-48000": "30k_48k",
        "latest.cost.net_price.{}.by_income_level.48001-75000": "48k_75k",
        "latest.cost.net_price.{}.by_income_level.75001-110000": "75k_110k",
        "latest.cost.net_price.{}.by_income_level.110001-plus": "110k_plus",
    }
    public_slices = {
        key.format("public"): val for key, val in slice_map.items()
    }
    private_slices = {
        key.format("private"): val for key, val in slice_map.items()
    }
    if school.control == "Public":
        mapping = public_slices
        school.avg_net_price = api_data.get("latest.cost.avg_net_price.public")
    else:
        mapping = private_slices
        school.avg_net_price = api_data.get(
            "latest.cost.avg_net_price.private"
        )
    for key, val in mapping.items():
        slice_data[val] = api_data.get(key)
    school.avg_net_price_slices = slice_data
    return school


def update(exclude_ids=None, single_school=None, store_programs=False):
    """
    Update college-level data for the latest year.

    Optionally, you can store program data and limit actions to one school.
    """

    if exclude_ids is None:
        exclude_ids = []

    programs_created = 0

    excluded_ids = OFFICE_IDS + FAKE_SCHOOL_PKS + exclude_ids
    no_data = []  # API failed to respond or provided no data
    closed = []  # schools that have closed since our last scrape
    job_msg = (
        "The job is paced to be friendly to the Scorecard API, "
        "so it can take an hour to run.\n"
        "A dot means a school was updated; a dash means no data found."
    )
    starter = datetime.datetime.now()
    processed = 0
    update_count = 0
    id_url = "{}&id={}&fields={}"
    base_query = School.objects.exclude(pk__in=excluded_ids)
    if single_school:
        if not base_query.filter(pk=single_school).exists():
            no_school_msg = "Could not find school with ID {}".format(
                single_school
            )
            return (no_data, no_school_msg)
        base_query = base_query.filter(pk=single_school)
        logger.info("Updating {}".format(base_query[0]))
    else:
        logger.info(
            "Seeking updates for {} schools.".format(base_query.count())
        )
        logger.info(job_msg)
    for school in base_query:
        processed += 1
        if processed % 500 == 0:  # pragma: no cover
            logger.info("\n{}\n".format(processed))
        if processed % 5 == 0:
            time.sleep(1)
        url = id_url.format(ID_BASE, school.school_id, FIELDSTRING)
        data = get_scorecard_data(url)
        if not data:
            no_data.append(school)
            sys.stdout.write("-")
            sys.stdout.flush()
            continue
        sys.stdout.write(".")
        sys.stdout.flush()
        update_count += 1
        if data.get("school.operating") == 0:
            school.operating = False
            school.save()
            closed.append(school)
            continue
        data["school.operating"] = True
        for key in DECIMAL_MAP:
            if data.get(key) is not None:
                setattr(school, DECIMAL_MAP[key], Decimal(str(data[key])))
        for key in MODEL_MAP:
            if data.get(key) is not None:
                setattr(school, MODEL_MAP[key], data[key])
        if data.get("school.ownership"):
            school.ownership = str(data["school.ownership"])
            school.control = CONTROL_MAP[school.ownership]
        set_school_grad_rate(school, data)
        compile_net_prices(school, data)
        program_data = api_utils.compile_school_programs(data)
        if program_data and type(program_data.get("most_popular")) == list:
            school.program_most_popular = program_data["most_popular"]
            school.program_count = program_data.get("program_count")
        school.zip5 = fix_zip5(str(school.zip5))
        school.save()
        if store_programs:
            programs_created += update_programs(data, school)
    endmsg = """
    Updated {} schools and found no data for {}\n\
    Schools that closed since last run: {}\n\
    \n{} took {} to run""".format(
        update_count,
        len(no_data),
        len(closed),
        SCRIPTNAME,
        (datetime.datetime.now() - starter),
    )
    if programs_created:
        logger.info("\nCreated {} program records".format(programs_created))
    if no_data:
        logger.info(
            "\n\nSchools for which we found no data on {}:".format(
                datetime.date.today().strftime("%b %-d, %Y")
            )
        )
        for school in no_data:
            logger.info("- {}".format(school))
    if closed:
        logger.info("\n\nSchools that have closed since the last update:")
        for school in closed:
            logger.info("- {}".format(school))
    return (no_data, endmsg)
