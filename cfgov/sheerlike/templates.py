import datetime
from dateutil import parser
from pytz import timezone


def _convert_date(date, tz):
    if date and isinstance(date, basestring):
        date = parser.parse(date,
                            default=datetime.datetime.today().replace(day=1))
    return date


def get_date_string(date, format="%Y-%m-%d", tz='America/New_York'):
    dt = _convert_date(date, tz)
    return dt.strftime(format)


def get_date_obj(date, tz='America/New_York'):
    dt = _convert_date(date, tz)
    return dt
