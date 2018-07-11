import datetime

from pytz import timezone

from .templates import _convert_date


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
