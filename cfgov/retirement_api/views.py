import json
import os

from django.http import HttpResponse, HttpResponseBadRequest

from dateutil import parser

from .utils.ss_calculator import get_retire_data
from .utils.ss_utilities import get_retirement_age


BASEDIR = os.path.dirname(__file__)


def param_check(request, param):
    if param in request.GET and request.GET[param]:
        return request.GET[param]
    else:
        return None


def income_check(param):
    cleaned = param.replace("$", "").replace(",", "").partition(".")[0]
    try:
        clean_income = int(cleaned)
    except ValueError:
        return None
    else:
        return clean_income


def estimator(request, dob=None, income=None, language="en"):
    ssa_params = {
        "dobmon": 0,
        "dobday": 0,
        "yob": 0,
        "earnings": 0,
        "lastYearEarn": "",  # not using
        "lastEarn": "",  # not using
        "retiremonth": "",  # only using for past-FRA users
        "retireyear": "",  # only using for past-FRA users
        "dollars": 1,  # benefits to be calculated in current-year dollars
        "prgf": 2,
    }
    if dob is None:
        dob = param_check(request, "dob")
        if not dob:
            return HttpResponseBadRequest("invalid date of birth")
    if income is None:
        income_raw = param_check(request, "income")
        if not income_raw:
            return HttpResponseBadRequest("invalid income")
        else:
            income = income_check(income_raw)
            if income is None:
                return HttpResponseBadRequest("invalid income")
    else:
        income = income_check(income)
        if income is None:
            return HttpResponseBadRequest("invalid income")
    try:
        dob_parsed = parser.parse(dob)
    except ValueError:
        return HttpResponseBadRequest("invalid date of birth")
    else:
        DOB = dob_parsed.date()
    ssa_params["dobmon"] = DOB.month
    ssa_params["dobday"] = DOB.day
    ssa_params["yob"] = DOB.year
    ssa_params["earnings"] = income
    data = get_retire_data(ssa_params, language)
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_full_retirement_age(request, birth_year):
    data_tuple = get_retirement_age(birth_year)
    if not data_tuple:
        return HttpResponseBadRequest("bad birth year (%s)" % birth_year)
    else:
        data = json.dumps(data_tuple)
        return HttpResponse(data, content_type="application/json")
