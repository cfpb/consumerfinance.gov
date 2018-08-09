import datetime
from six import string_types as basestring

from django.utils.timezone import template_localtime

from dateutil import parser
from jinja2.ext import Extension
from pytz import timezone

from v1.util.util import extended_strftime


def date_formatter(dt, text_format=False):
    format = '%_m %_d, %Y' if text_format else '%b %d, %Y'
    return extended_strftime(dt, format)


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


def when(starttime, endtime, streamtime=None):
    start = _convert_date(starttime, 'America/New_York')
    if streamtime:
        start = _convert_date(streamtime, 'America/New_York')
    end = _convert_date(endtime, 'America/New_York')
    if start > datetime.datetime.now(timezone('America/New_York')):
        return 'future'
    elif end < datetime.datetime.now(timezone('America/New_York')):
        return 'past'
    else:
        return 'present'


class DatetimesExtension(Extension):
    def __init__(self, environment):
        super(DatetimesExtension, self).__init__(environment)
        self.environment.globals.update({
            'date_formatter': date_formatter,
            'localtime': template_localtime,
            'when': when,
        })

        self.environment.filters.update({
            'date': get_date_string,
            'localtime': template_localtime,
        })
