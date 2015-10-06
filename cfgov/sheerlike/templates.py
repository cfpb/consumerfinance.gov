import datetime
from dateutil import parser
from pytz import timezone

def date_formatter(value, format="%Y-%m-%d", tz='America/New_York'):
    if type(value) not in [datetime.datetime, datetime.date]:
        date = parser.parse(value, default=datetime.datetime.today().replace(day=1))
        naive = date.replace(tzinfo=None)
        dt = timezone(tz).localize(naive)
    else:
        dt = value

    return dt.strftime(format)
