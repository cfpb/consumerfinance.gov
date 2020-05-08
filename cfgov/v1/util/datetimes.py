import datetime

from dateutil import parser
from pytz import timezone


def convert_date(date, tz):
    """ Takes a string or datetime and a timezone, returns aware datetime

    If the passed `date` is a string, it first converts that to a naive
    datetime. Then (and if `date` was already a datetime), it takes the passed
    timezone and converts the datetime to one that is in that timezone.
    """
    if date and isinstance(date, str):
        date = parser.parse(
            date,
            default=datetime.datetime.today().replace(day=1)
        )
    if isinstance(date, datetime.datetime) and tz:
        this_tz = timezone(tz)
        if date.tzinfo is None:
            return this_tz.localize(date)
        return date.astimezone(this_tz)
    return date
