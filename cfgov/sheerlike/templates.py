import datetime

from dateutil import parser
from pytz import timezone


def _convert_date(date, tz):
    if date and isinstance(date, basestring):
        date = parser.parse(date,
                            default=datetime.datetime.today().replace(day=1))
    if isinstance(date, datetime.datetime) and tz:
        this_tz = timezone(tz)
        if date.tzinfo is None:
            return this_tz.localize(date)
        return date.astimezone(this_tz)
    return date


def get_date_string(date, format="%Y-%m-%d", tz='America/New_York'):
    dt = _convert_date(date, tz)
    return dt.strftime(format)


def get_date_obj(date, tz='America/New_York'):
    dt = _convert_date(date, tz)
    return dt
