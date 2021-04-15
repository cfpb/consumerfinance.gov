from datetime import date, datetime

from dateutil import parser, relativedelta
from pytz import timezone


# This utility file exists to support date input fields that are typeable
# text inputs, which occur in browsers that don't support the date input field
# https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/date

# For more information on date formatting, see the python documentation here:
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

def convert_date(date, tz):
    """ Takes a string or datetime and a timezone, returns aware datetime

    If the passed `date` is a string, it first converts that to a naive
    datetime. Then (and if `date` was already a datetime), it takes the passed
    timezone and converts the datetime to one that is in that timezone.
    """
    if date and isinstance(date, str):
        date = parser.parse(
            date,
            default=datetime.today().replace(day=1)
        )
    if isinstance(date, datetime) and tz:
        this_tz = timezone(tz)
        if date.tzinfo is None:
            return this_tz.localize(date)
        return date.astimezone(this_tz)
    return date


def date_from_pattern(date_str, pattern):
    try:
        return datetime.strptime(date_str, pattern).date()
    except (ValueError, TypeError):
        return None


def end_of_time_period(user_input, input_date):
    for pattern in ('%m/%d/%Y', '%m-%d-%Y', '%m/%d/%y', '%m-%d-%y'):
        if date_from_pattern(user_input, pattern) is not None:
            return input_date
    for pattern in ('%m/%Y', '%m-%Y', '%m/%y', '%m-%y'):
        if date_from_pattern(user_input, pattern) is not None:
            return input_date + relativedelta(day=31)
    for pattern in ('%Y'):
        if date_from_pattern(user_input, pattern) is not None:
            return date(input_date.year, 12, 31)
    return input_date
