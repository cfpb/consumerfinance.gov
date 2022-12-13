from django.utils.timezone import template_localtime

from jinja2.ext import Extension

from v1.util.datetimes import convert_date
from v1.util.util import extended_strftime


def date_formatter(dt, text_format=False):
    format = "%_m %_d, %Y" if text_format else "%b %d, %Y"
    return extended_strftime(dt, format)


def get_date_string(date, format="%Y-%m-%d", tz="America/New_York"):
    dt = convert_date(date, tz)
    return dt.strftime(format)


class DatetimesExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        self.environment.globals.update(
            {
                "date_formatter": date_formatter,
                "localtime": template_localtime,
            }
        )

        self.environment.filters.update(
            {
                "date": get_date_string,
                "localtime": template_localtime,
            }
        )
