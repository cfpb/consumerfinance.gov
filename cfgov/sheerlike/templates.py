import datetime
from dateutil import parser
from pytz import timezone


def _convert_date(date, tz):
    if date:
        if isinstance(date, basestring):
            date = parser.parse(date,
                                default=datetime.datetime.today().replace(day=1))
        if type(date) in [datetime.datetime, datetime.date]:
            if isinstance(date, datetime.datetime):
                pytzone = timezone(tz)
                if date.tzinfo:
                    date = date.replace(tzinfo=None)
                date = pytzone.localize(date)
    return date


def get_date_string(date, format="%Y-%m-%d", tz='America/New_York'):
    dt = _convert_date(date, tz)
    return dt.strftime(format)


def get_date_obj(date, tz='America/New_York'):
    dt = _convert_date(date, tz)
    return dt
