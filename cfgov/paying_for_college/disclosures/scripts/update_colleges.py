"""Update college data using the Dept. of Education's collegechoice api"""
import datetime
import logging
import os
import sys
import time
from decimal import Decimal

import requests
from paying_for_college.disclosures.scripts import api_utils
from paying_for_college.disclosures.scripts.api_utils import (
    DECIMAL_MAP, MODEL_MAP
)
from paying_for_college.models import CONTROL_MAP, FAKE_SCHOOL_PK, School


logger = logging.getLogger(__name__)

DATESTAMP = datetime.datetime.now().strftime("%Y-%m-%d")
HOME = os.path.expanduser("~")
NO_DATA_FILE = "{}/no_data_{}.json".format(HOME, DATESTAMP)
SCRIPTNAME = os.path.basename(__file__).partition('.')[0]
ID_BASE = "{}?api_key={}".format(api_utils.SCHOOLS_ROOT, api_utils.API_KEY)
FIELDS = sorted(MODEL_MAP.keys())
FIELDSTRING = api_utils.build_field_string()


def fix_zip5(zip5):
    """add leading zeros if they have been stripped by the scorecard db"""
    if len(zip5) == 4:
        return "0{}".format(zip5)
    if len(zip5) == 3:
        return "00{}".format(zip5)
    else:
        return zip5[:5]


def get_scorecard_data(url):
    response = requests.get(url)
    if not response.ok:
        logger.info("request not OK, returned {}".format(response.reason))
        if response.status_code == 429:
            logger.info("API limit reached")
        return
    if not response.json() or not response.json().get('results'):
        return
    return response.json().get('results')[0]


def set_school_grad_rate(school, api_data):
    """Set the appropriate grad rate for a given school."""
    four_year_raw = api_data.get(
        'latest.completion.completion_rate_4yr_150nt_pooled')
    associate_raw = api_data.get(
        'latest.completion.completion_rate_less_than_4yr_150nt_pooled')
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


def update(exclude_ids=[], single_school=None):
    """update college-level data for the latest year"""

    exclude_ids += [FAKE_SCHOOL_PK]
    NO_DATA = []  # API failed to respond or provided no data
    CLOSED = []  # schools that have closed since our last scrape
    START_MSG = "Requesting latest school data."
    JOB_MSG = (
        "The job is paced to be friendly to the Scorecard API, "
        "so it can take an hour to run.\n"
        "A dot means a school was updated; a dash means no data found.")
    logger.info(START_MSG)
    if not single_school:
        logger.info(JOB_MSG)
    STARTER = datetime.datetime.now()
    PROCESSED = 0
    UPDATE_COUNT = 0
    id_url = "{}&id={}&fields={}"
    base_query = School.objects.exclude(pk__in=exclude_ids)
    if single_school:
        base_query = base_query.filter(pk=single_school)
        logger.info("Updating {}".format(base_query[0]))
    else:
        base_query = base_query.filter(operating=True)
    for school in base_query:
        UPDATED = False
        PROCESSED += 1
        if PROCESSED % 500 == 0:  # pragma: no cover
            logger.info("\n{}\n".format(PROCESSED))
        if PROCESSED % 5 == 0:
            time.sleep(1)
        url = id_url.format(ID_BASE, school.school_id, FIELDSTRING)
        data = get_scorecard_data(url)
        if not data:
            NO_DATA.append(school)
            sys.stdout.write('-')
            sys.stdout.flush()
            continue
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
            if data.get('school.operating') == 0:
                school.operating = False
                school.save()
                CLOSED.append(school)
                continue
            else:
                data['school.operating'] = True
            for key in DECIMAL_MAP:
                if data.get(key) is not None:
                    setattr(school, DECIMAL_MAP[key], Decimal(str(data[key])))
                    UPDATED = True
            for key in MODEL_MAP:
                if data.get(key) is not None:
                    setattr(school, MODEL_MAP[key], data[key])
                    UPDATED = True
            if data.get('school.ownership'):
                school.ownership = str(data['school.ownership'])
                school.control = CONTROL_MAP[school.ownership]
            school = set_school_grad_rate(school, data)
            program_data = api_utils.compile_school_programs(data)
            if program_data and type(program_data.get('most_popular')) == list:
                UPDATED = True
                school.program_most_popular = program_data['most_popular']
                school.program_count = program_data.get(
                    'program_count')
            if UPDATED is True:
                UPDATE_COUNT += 1
                school.zip5 = fix_zip5(str(school.zip5))
                school.save()
    endmsg = """
    Updated {} schools and found no data for {}\n\
    Schools that closed since last run: {}\n\
    \n{} took {} to run""".format(
        UPDATE_COUNT,
        len(NO_DATA),
        len(CLOSED),
        SCRIPTNAME,
        (datetime.datetime.now() - STARTER))
    if NO_DATA:
        logger.info("\n\nSchools for which we found no data:")
        for school in NO_DATA:
            logger.info("- {} ({})".format(school.primary_alias, school.pk))
    if CLOSED:
        logger.info("\n\nSchools that have closed since the last update:")
        for school in CLOSED:
            logger.info("- {} ({})".format(school.primary_alias, school.pk))

    return (NO_DATA, endmsg)
