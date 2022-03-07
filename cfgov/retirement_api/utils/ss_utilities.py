# coding: utf-8
import datetime
import json
import logging
import os

from dateutil import parser


TODAY = datetime.datetime.now().date()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TOO_YOUNG = """\
<span class="h4">Sorry, our tool cannot provide an estimate \
if you are under 22 years of age.</span> Please visit the \
Social Security Administration's \
<a href="http://www.ssa.gov/people/youngpeople/" \
target="_blank" rel="noopener noreferrer">advice page</a> \
for students and younger workers.\
"""
TOO_YOUNG_ES = """\
Lo sentimos. No podemos estimar sus beneficios si usted \
es menor de 22 años de edad.</span> \
Visite <a href="http://www.ssa.gov/people/youngpeople/" \
target="_blank" rel="noopener noreferrer">la página</a> \
(en inglés) de la Administración \
del Seguro Social para estudiantes y trabajadores jóvenes.\
"""
TOO_OLD = """\
<span class="h4">Sorry, our tool cannot provide an estimate because \
your birthdate, {0}, means you are older than 70 and may already be receiving \
benefits.</span> To check your benefits based on your actual \
earnings record, contact the Social Security Administration or \
open a <a href="http://www.socialsecurity.gov/myaccount/" \
target="_blank" rel="noopener noreferrer">\
<em>my</em> Social Security</a> account.\
"""
TOO_OLD_ES = """\
<span class="h4">Lo sentimos. No podemos estimar sus beneficios ya que \
la fecha de nacimiento que ingresó, {0}, significa que usted \
es mayor de 70 años de edad y posiblemente ya recibe beneficios. </span>\
Verifique sus beneficios basados en su propio registro de ingresos \
del Seguro Social \
<a href="http://www.ssa.gov/espanol/jubilacion2/calculadora.html" \
target="_blank" rel="noopener noreferrer">aquí</a> o \
<a href="http://www.socialsecurity.gov/espanol/agencia/contacto/" \
target="_blank" rel="noopener noreferrer">comuníquese</a> \
con la Administración del Seguro Social.\
"""

AGE_ERROR_NOTES = {
    "too_old": {"en": TOO_OLD, "es": TOO_OLD_ES},
    "too_young": {"en": TOO_YOUNG, "es": TOO_YOUNG_ES},
}


def get_note(note_type, language):
    """return language_specific error"""
    if language == "es":
        return AGE_ERROR_NOTES[note_type]["es"]
    else:
        return AGE_ERROR_NOTES[note_type]["en"]


# this datafile specifies years that have unique retirement age values
# since this may change, it is maintained in an external file
datafile = "{0}\
/retirement_api/data/unique_retirement_ages.json".format(
    BASE_DIR
)

with open(datafile, "r") as f:
    age_map = json.loads(f.read())
    for year in age_map:
        age_map[year] = tuple(age_map[year])


def get_current_age(dob):
    today = datetime.date.today()
    if type(dob) == datetime.date:
        DOB = dob
    else:
        try:
            DOB = parser.parse(dob).date()
        except (TypeError, ValueError):
            return None
    if DOB < today:
        try:  # when dob is 2/29 and the current year is not a leap year
            birthday = DOB.replace(year=today.year)
        except ValueError:
            birthday = DOB.replace(year=today.year, day=DOB.day - 1)
        if birthday > today:
            return today.year - DOB.year - 1
        else:
            return today.year - DOB.year
    else:
        return None


def get_months_past_birthday(dob):
    """return the number of months a person is past their last birthday"""
    today = datetime.date.today()
    months_at_birth = dob.year * 12 + dob.month - 1
    months_today = today.year * 12 + today.month - 1
    delta = months_today - months_at_birth
    return delta % 12


def get_months_until_next_birthday(dob):
    """return number of months until next birthday, with a minimum of 1"""
    today = datetime.date.today()
    try:
        bday_this_year = datetime.date(today.year, dob.month, dob.day)
    except ValueError:
        # Handle Leap Day birthdays
        bday_this_year = datetime.date(today.year, dob.month, dob.day - 1)

    if today >= bday_this_year:
        return (12 - today.month) + dob.month
    elif today < bday_this_year:
        months_until = dob.month - today.month
        if months_until == 0:
            return 1
        else:
            return months_until


def yob_test(yob=None):
    """
    tests to make sure suppied birth year is valid;
    returns valid birth year as a string or None
    """
    log = logging.getLogger(__name__)
    today = datetime.datetime.now().date()
    if not yob:
        return None
    try:
        birth_year = int(yob)
    except (TypeError, ValueError):
        log.warn("birth year should be a number")
        return None
    else:
        b_string = str(birth_year)
        if birth_year > today.year:
            log.warn("can't work with birth dates in the future")
            return None
        elif len(b_string) != 4:
            log.warn("please supply a 4-digit birth year")
            return None
        else:
            return b_string


def get_retirement_age(birth_year):
    """
    given a worker's birth year,
    returns full retirement age in years and months;
    returns None if the supplied year isn't valid
    """
    b_string = yob_test(birth_year)
    if b_string:
        yob = int(birth_year)
        if b_string in age_map.keys():
            return age_map[b_string]
        elif yob <= 1937:
            return (65, 0)
        elif yob >= 1943 and yob <= 1954:
            return (66, 0)
        elif yob >= 1960:
            return (67, 0)
    else:
        return None


def past_fra_test(dob=None, language="en"):
    """
    tests whether a person is past his/her full retirement age
    """
    if not dob:
        return "invalid birth date entered"
    try:
        DOB = parser.parse(dob).date()
    except (TypeError, ValueError):
        return "invalid birth date entered"
    today = datetime.date.today()
    current_age = get_current_age(dob)
    if DOB >= today:
        return get_note("too_young", language)
    # SSA has a special rule for people born on Jan. 1
    # http://www.socialsecurity.gov/OACT/ProgData/nra.html
    if DOB.month == 1 and DOB.day == 1:
        fra_tuple = get_retirement_age(DOB.year - 1)
    else:
        fra_tuple = get_retirement_age(DOB.year)
    age_tuple = (current_age, get_months_past_birthday(DOB))
    # print "age_tuple: %s; fra_tuple: %s" % (age_tuple, fra_tuple)
    if age_tuple[0] < 22:
        return get_note("too_young", language)
    if age_tuple[0] > 70:
        return get_note("too_old", language).format(DOB.strftime("%m/%d/%Y"))
    if age_tuple[0] > fra_tuple[0]:
        return True
    elif age_tuple[0] < fra_tuple[0]:
        return False
    elif age_tuple[0] == fra_tuple[0] and age_tuple[1] >= fra_tuple[1]:
        return True
    else:  # pragma: no cover -- can't currently happen, but could in future
        return False


def get_delay_bonus(birth_year):
    """
    given a worker's year of birth,
    returns the annual bonus for delaying retirement
    past full retirement age
    """
    b_string = yob_test(birth_year)
    if b_string:
        yob = int(birth_year)
        if yob in [1933, 1934]:
            return 5.5
        elif yob in [1935, 1936]:
            return 6.0
        elif yob in [1937, 1938]:
            return 6.5
        elif yob in [1939, 1940]:
            return 7.0
        elif yob in [1941, 1942]:
            return 7.5
        elif yob >= 1943:
            return 8.0
        else:
            return None
