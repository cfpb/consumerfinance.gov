# coding: utf-8
"""
A utility to get benefit data from SSA and handle errors.

Users must be at least 22 to use the form.
Users past their full retirement age will get results only
 for their current year and any other years up to 70.
We ask users only for DOB and current annual earnings.
Benefit values for all years are shown in today's dollars

Inputs:
- date of birth
- annual earnings

Optional inputs that SSA allows, but we're not using:
- Last year with earnings
- Last earnings
- Benefit in inflated dollars; we're using default of current-year dollars

Outputs:
- a python dictionary of benefit data and error messages
"""
import datetime
import logging
import re
from datetime import date

import requests
from bs4 import BeautifulSoup as bs
from dateutil import parser

from .ss_utilities import (
    get_current_age, get_months_past_birthday, get_months_until_next_birthday,
    get_retirement_age, past_fra_test
)


TIMEOUT_SECONDS = 20
LOGGER = logging.getLogger(__name__)

down_note = """<span class="h4">Sorry, the Social Security website \
is not responding, so we can't estimate your benefits.</span> \
Please try again in a few minutes."""

down_note_es = """<span class="h4">Lo sentimos. En este momento no podemos \
generar un estimado ya que la calculadora no está respondiendo.</span> \
Vuelva en un par de minutos."""

no_earnings_note = """<span class="h4">Sorry, we cannot provide an estimate \
because your entered annual income is less than \
the minimum needed to make the estimate.</span>"""

no_earnings_note_es = """<span class="h4">Lo sentimos. \
No podemos estimar sus beneficios, ya que su ingreso anual es menor \
que la cantidad necesaria para poder generar un cálculo aproximado \
de sus beneficios.</span>"""

ERROR_NOTES = {
    "down": {"en": down_note, "es": down_note_es},
    "earnings": {"en": no_earnings_note, "es": no_earnings_note_es},
}

PAST_NOTE = "Age {0} is past your full benefit claiming age."
NO_DISABILITY_NOTE = "You have reached full retirement age \
and are not eligible for disability benefits."


def get_note(note_type, language):
    """return language_specific error"""
    if language == "es":
        return ERROR_NOTES[note_type]["es"]
    else:
        return ERROR_NOTES[note_type]["en"]


# ORIGINAL_BASE_URL = "https://www.socialsecurity.gov  # NOW REDIRECTED"
# QUICK_URL = "{0}/OACT/quickcalc/".format(BASE_URL)  # where users go
BASE_URL = "https://www.ssa.gov"
RESULT_URL = "{0}/cgi-bin/benefit6.cgi".format(BASE_URL)
CHART_AGES = range(62, 71)

comment = re.compile(r"<!--[\s\S]*?-->")  # regex for parsing indexing data


def clean_comment(comment):
    return comment.replace("<!--", "").replace("-->", "").strip()


# calculation constants
EARLY_PENALTY = 0.00555555  # monthly penalty for months closest to FRA
EARLIER_PENALTY = 0.004166666  # monthly penalty for earliest claiming ages
MONTHLY_BONUS = 0.00667  # bonus value for each month's delay past FRA
ANNUAL_BONUS = 0.08  # annual bonus value for each year's delay past FRA


def num_test(value=""):
    try:
        int(value)
    except ValueError:
        try:
            int(float(value))
        except ValueError:
            LOGGER.info("Numeric test failed for {}".format(value))
            return False
        else:
            return True
    else:
        return True


# unused for now
def parse_details(rows):
    datad = {}
    if len(rows) == 3:
        titlerow = rows[0].split(":")
        datad[titlerow[0].strip().upper()] = {
            "Bend points": titlerow[1].strip()
        }
        outer = datad[titlerow[0].strip().upper()]
        outer["AIME"] = rows[1]
        outer["COLA"] = rows[2]
    return datad


def calculate_lifetime_benefits(results, base, fra_tuple, dob, past_fra):
    """Add lifetime benefit values for each year shown in bar graph"""
    AGE = results["current_age"]
    BENS = results["data"]["benefits"]
    LIFE = results["data"]["lifetime"] = {}
    for year in range(62, 71):
        benkey = "age {0}".format(year)
        lifekey = "age{0}".format(year)
        if BENS[benkey] == 0:
            LIFE[lifekey] = 0
        else:
            bar_value = BENS[benkey]
            max_months = (85 - year) * 12
            max_benefit = max_months * bar_value
            if year == AGE:
                month_adjustment = results["data"]["months_past_birthday"]
                if year == 62 and month_adjustment == 0 and dob.day != 2:
                    month_adjustment = 1
                life_benefit = max_benefit - (month_adjustment * bar_value)
            elif year == 62:
                if dob.day == 2:  # born-on-2nd edge case
                    life_benefit = max_benefit
                else:
                    life_benefit = max_benefit - bar_value
            elif year == fra_tuple[0]:
                month_adjustment = fra_tuple[1]
                life_benefit = max_benefit - (month_adjustment * bar_value)
            else:
                life_benefit = max_benefit
            LIFE[lifekey] = life_benefit
    return results


def interpolate_benefits(results, base, fra_tuple, current_age, DOB):
    """
    Calculate benefits for years above and below the full-retirement age (FRA).

    This function is only for people who are below full retirement age.
    Those born on 2nd of month have a bigger early-claiming penalty max.
    Those born on 1st of month and have have an FRA with a month value
    need special handling.
    """
    BENS = results["data"]["benefits"]
    # today = datetime.date.today()
    # current_year_bd = datetime.date(today.year, DOB.month, DOB.day)
    # months_past_birthday = get_months_past_birthday(DOB)
    (fra, fra_months) = fra_tuple
    # the first step can be affected by the full-retirement-age months value
    initial_months_forward = 12 - fra_months
    initial_months_back = 12 + fra_months  # months to apply the bigger penalty
    # for people whose current age is withing the graph,
    # the final reduction depends on the subject's current age
    # final_months_back = 12 - months_past_birthday
    # fill out the missing years, working backward and forward from the FRA
    if fra == 67:  # subject is 56 or younger, so age is not within the graph
        base = BENS["age 67"]
        if DOB.day == 2:  # the born-on-the-2nd edge case
            BENS["age 62"] = int(
                round(
                    base
                    - base * (3 * 12 * EARLY_PENALTY)
                    - base * (2 * 12 * EARLIER_PENALTY)
                )
            )
        else:
            BENS["age 62"] = int(
                round(
                    base
                    - base * (3 * 12 * EARLY_PENALTY)
                    - base * (12 * EARLIER_PENALTY)
                    - base * (11 * EARLIER_PENALTY)
                )
            )
        BENS["age 63"] = int(
            round(
                base
                - base * (3 * 12 * EARLY_PENALTY)
                - base * (12 * EARLIER_PENALTY)
            )
        )
        BENS["age 64"] = int(round(base - base * (3 * 12 * EARLY_PENALTY)))
        BENS["age 65"] = int(round(base - base * (2 * 12 * EARLY_PENALTY)))
        BENS["age 66"] = int(round(base - base * (1 * 12 * EARLY_PENALTY)))
        BENS["age 68"] = int(round(base + (base * ANNUAL_BONUS)))
        BENS["age 69"] = int(round(base + (2 * (base * ANNUAL_BONUS))))
        BENS["age 70"] = int(round(base + (3 * (base * ANNUAL_BONUS))))
    elif fra == 66:  # DOB is 1/1/1960 or before
        base = BENS["age 66"]
        annual_bump = round(base * ANNUAL_BONUS)
        monthly_bump = base * MONTHLY_BONUS
        first_bump = round(monthly_bump * initial_months_forward)
        monthly_penalty = base * EARLY_PENALTY
        earlier_monthly_penalty = base * EARLIER_PENALTY
        dob_month_delta = 12 - get_months_past_birthday(DOB)
        first_penalty = initial_months_back * monthly_penalty
        BENS["age 67"] = int(base + first_bump)
        BENS["age 68"] = int(base + first_bump + annual_bump)
        BENS["age 69"] = int(base + first_bump + (2 * annual_bump))
        BENS["age 70"] = int(base + first_bump + (3 * annual_bump))
        if current_age == 65:
            BENS["age 62"] = 0
            BENS["age 63"] = 0
            BENS["age 64"] = 0
            BENS["age 65"] = int(
                round(base - (dob_month_delta * monthly_penalty))
            )
        elif current_age == 64:
            BENS["age 62"] = 0
            BENS["age 63"] = 0
            BENS["age 64"] = int(
                round(
                    base - first_penalty - (dob_month_delta * monthly_penalty)
                )
            )
            BENS["age 65"] = int(round(base - first_penalty))
        elif current_age == 63:
            BENS["age 62"] = 0
            BENS["age 63"] = int(
                round(
                    base
                    - first_penalty
                    - (12 * monthly_penalty)
                    - (dob_month_delta * monthly_penalty)
                )
            )
            BENS["age 64"] = int(
                round(base - first_penalty - (12 * monthly_penalty))
            )
            BENS["age 65"] = int(round(base - first_penalty))
        elif current_age == 62:
            BENS["age 62"] = int(
                round(
                    base
                    - first_penalty
                    - (2 * 12 * monthly_penalty)
                    - (dob_month_delta * earlier_monthly_penalty)
                )
            )
            BENS["age 63"] = int(
                round(base - first_penalty - (2 * 12 * monthly_penalty))
            )
            BENS["age 64"] = int(
                round(base - first_penalty - (12 * monthly_penalty))
            )
            BENS["age 65"] = int(round(base - first_penalty))
        elif current_age in range(55, 62):
            if DOB.day == 2:
                BENS["age 62"] = int(
                    round(
                        base
                        - first_penalty
                        - (12 * monthly_penalty)
                        - ((12 - fra_months) * monthly_penalty)
                        - (fra_months * earlier_monthly_penalty)
                        - (12 * earlier_monthly_penalty)
                    )
                )
            else:
                BENS["age 62"] = int(
                    round(
                        base
                        - first_penalty
                        - (12 * monthly_penalty)
                        - ((12 - fra_months) * monthly_penalty)
                        - (fra_months * earlier_monthly_penalty)
                        - (11 * earlier_monthly_penalty)
                    )
                )
            BENS["age 63"] = int(
                round(
                    base
                    - first_penalty
                    - (12 * monthly_penalty)
                    - ((12 - fra_months) * monthly_penalty)
                    - (fra_months * earlier_monthly_penalty)
                )
            )
            BENS["age 64"] = int(
                round(base - first_penalty - (12 * monthly_penalty))
            )
            BENS["age 65"] = int(round(base - first_penalty))
    return results


def interpolate_for_past_fra(results, base, current_age, dob):
    """
    Calculate future benefits people who have passed full retirement age.
    Handles edge case when subject's born on 1st and birthday is in same month.
    """
    # today = datetime.date.today()
    BENS = results["data"]["benefits"]
    annual_bump = round(base * ANNUAL_BONUS)
    monthly_bump = base * MONTHLY_BONUS
    first_bump = round(monthly_bump * get_months_until_next_birthday(dob))
    if get_months_past_birthday(dob) == 11 and dob.day == 1:
        results["params_adjusted"] = True
        current_age = current_age + 1
        results["current_age"] = current_age
        results["note"] = PAST_NOTE.format(current_age)
        results["data"]["months_past_birthday"] = 0
        first_bump = annual_bump
    if current_age == 66:
        BENS["age 66"] = base
        BENS["age 67"] = base + first_bump
        BENS["age 68"] = base + first_bump + annual_bump
        BENS["age 69"] = base + first_bump + (2 * annual_bump)
        BENS["age 70"] = base + first_bump + (3 * annual_bump)
    elif current_age == 67:
        BENS["age 67"] = base
        BENS["age 68"] = base + first_bump
        BENS["age 69"] = base + first_bump + annual_bump
        BENS["age 70"] = base + first_bump + (2 * annual_bump)
    elif current_age == 68:
        BENS["age 68"] = base
        BENS["age 69"] = base + first_bump
        BENS["age 70"] = base + first_bump + annual_bump
    elif current_age == 69:
        BENS["age 69"] = base
        BENS["age 70"] = base + first_bump
    elif current_age == 70:
        BENS["age 70"] = base
    return results


# # sample params
# params = {
#     'dobmon': 8,
#     'dobday': 14,
#     'yob': 1970,
#     'earnings': 70000,
#     'lastYearEarn': '',  # possible use for unemployed or already retired
#     'lastEarn': '',  # possible use for unemployed or already retired
#     'retiremonth': '',  # used to get consistent results from calculator
#     'retireyear': '',  # used to get consistent results from calculator
#     'dollars': 1,  # benefits to be calculated in current-year dollars
#     'prgf': 2
# }


def set_up_runvars(params, language="en"):
    """
    Set up the results container and variables

    This function also sets up handling of the MM/01/YYYY edge case
    The returned vars 'dob' and 'dobstring' are original values;
    Other vars, such as current_age, and SSA params may be altered
      to match SSA's handling of edge cases
    """
    today = date.today()
    dobstring = "{0}-{1}-{2}".format(
        params["yob"], params["dobmon"], params["dobday"]
    )
    yobstring = "{0}".format(params["yob"])
    current_age = get_current_age(dobstring)
    dob = parser.parse(dobstring).date()
    benefits = {}
    for age in CHART_AGES:
        benefits["age {0}".format(age)] = 0
    results = {
        "data": {
            "months_past_birthday": get_months_past_birthday(dob),
            "early retirement age": "",
            "full retirement age": "",
            "benefits": benefits,
            "params": params,
            "disability": "",
            "survivor benefits": {
                "child": "",
                "spouse caring for child": "",
                "spouse at full retirement age": "",
                "family maximum": "",
            },
        },
        "current_age": current_age,
        "error": "",
        "note": "",
        "past_fra": "",
        "params_adjusted": False,
    }
    past_fra = past_fra_test(dobstring, language=language)
    if isinstance(past_fra, bool) is False:
        return (dob, dobstring, current_age, (0, 0), past_fra, results)
    else:
        results["past_fra"] = past_fra
    ssa_params = results["data"]["params"]
    if dob.day == 1:
        results["params_adjusted"] = True
        ssa_params["dobday"] = 2
        if dob.month == 1:
            yob = ssa_params["yob"] - 1
            yobstring = "{0}".format(yob)
            ssa_params["dobmon"] = 12
            ssa_params["yob"] = yob
        else:
            ssa_params["dobmon"] = params["dobmon"] - 1
    fra_tuple = get_retirement_age(yobstring)  # returns tuple: (year, months)
    if fra_tuple[1]:
        FRA = "{0} and {1} months".format(fra_tuple[0], fra_tuple[1])
    else:
        FRA = "{0}".format(fra_tuple[0])
    results["data"]["full retirement age"] = FRA
    if past_fra is True:
        ssa_params["retireyear"] = today.year
        ssa_params["retiremonth"] = today.month
        results["note"] = PAST_NOTE.format(current_age)
        results["data"]["disability"] = NO_DISABILITY_NOTE
    else:
        retire_year = ssa_params["yob"] + fra_tuple[0]
        retire_month = ssa_params["dobmon"] + fra_tuple[1]
        if retire_month > 12:
            retire_month = retire_month - 12
            retire_year += 1
        ssa_params["retireyear"] = retire_year
        ssa_params["retiremonth"] = retire_month
    return (dob, dobstring, current_age, fra_tuple, past_fra, results)


def parse_response(results, html, language):
    soup = bs(html, "html.parser")
    if soup.find("p") and "insufficient to receive" in soup.find("p").text:
        results["error"] = "benefit is zero"
        results["note"] = get_note("earnings", language)
        return (results, 0)
    ret_amount_raw = soup.find("span", {"id": "ret_amount"})
    if not ret_amount_raw:
        results["error"] = "bad response from SSA"
        results["note"] = get_note("down", language)
        return (results, 0)
    ret_amount = ret_amount_raw.text.split(".")[0].replace(",", "")
    base_benefit = int(ret_amount)
    return (results, base_benefit)


def validate_date(params):
    """Make sure delivered date is real"""
    dobstring = "{0}-{1}-{2}".format(
        params["yob"], params["dobmon"], params["dobday"]
    )
    try:
        parser.parse(dobstring).date()
        return True
    except ValueError:
        return False


def get_retire_data(params, language):
    """
    Get a base full-retirement-age benefit from SSA's Quick Calculator
    and interpolate benefits for other claiming ages, handling edge cases:
    - those past full retirement age
    - ages outside the parameters of our tool -- < 22 or > 70
    - users who enter earnings too low for benefits
    - those born on Jan. 1, see socialsecurity.gov/OACT/ProgData/nra.html
    - those born on 1st day of a month, considered born the previous month
    - those born on 1st day of a month and are within a month of next birthday
    - those born on 1st day of a month and whose full retirement age is
        66 plus a month value, such as 66 and 6 months
    - those born on 2nd day of a month, interpolator adds a month to reductions
    - dobs in 1950 that the Quick Calculator improperly treats as past FRA.
    """
    if not validate_date(params):
        return {"error": "An invalid date was entered."}

    starter = datetime.datetime.now()
    (
        dob,
        dobstring,
        current_age,
        fra_tuple,
        past_fra,
        results,
    ) = set_up_runvars(params, language=language)
    if isinstance(past_fra, bool) is False:
        # if past_fra is neither False nor True, there's an error and we bail
        if current_age and current_age > 70:
            results["past_fra"] = True
            results["note"] = past_fra
            results["error"] = "visitor too old for tool"
            return results
        elif current_age is None or current_age < 22:
            results["note"] = past_fra
            results["error"] = "visitor too young for tool"
            return results
        elif "invalid" in past_fra:  # pragma: no cover -- tested elsewhere
            results["note"] = "An invalid date was entered."
            results["error"] = past_fra
            return results
    try:
        req = requests.post(
            RESULT_URL, data=results["data"]["params"], timeout=TIMEOUT_SECONDS
        )
    except requests.exceptions.ConnectionError as e:
        results["error"] = "connection error at SSA's website: {0}".format(e)
        results["note"] = get_note("down", language)
        return results
    except requests.exceptions.Timeout:
        results["error"] = "SSA's website timed out"
        results["note"] = get_note("down", language)
        return results
    except requests.exceptions.RequestException as e:
        results["error"] = "request error at SSA's website: {0}".format(e)
        results["note"] = get_note("down", language)
        return results
    except Exception:
        results["error"] = "Unknown error at SSA's website"
        results["note"] = get_note("down", language)
        return results
    if not req.ok:
        ok_msg = "SSA's website is not responding. Status code: {0} ({1})"
        results["error"] = ok_msg.format(req.status_code, req.reason)
        results["note"] = get_note("down", language)
        return results
    (results, base_benefit) = parse_response(results, req.text, language)
    if results["error"]:
        return results
    if past_fra is True:
        results = interpolate_for_past_fra(
            results, base_benefit, current_age, dob
        )
    else:
        results["data"]["benefits"][
            "age {0}".format(fra_tuple[0])
        ] = base_benefit
        results = interpolate_benefits(
            results, base_benefit, fra_tuple, current_age, dob
        )
    final_results = calculate_lifetime_benefits(
        results, base_benefit, fra_tuple, dob, past_fra
    )
    LOGGER.info(
        "script took {0} to run".format((datetime.datetime.now() - starter))
    )
    return final_results
