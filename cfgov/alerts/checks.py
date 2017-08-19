import math
import ntplib

from django.conf import settings

from watchman.decorators import check


@check
def check_clock_drift():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request(
        settings.NTP_TIME_SERVER,
        version=3,
    )
    offset = settings.MAX_ALLOWED_TIME_OFFSET
    if math.fabs(response.offset) > offset:
        result = {
            'ok': False,
            'error': 'Clock has drifted more than {} seconds'.format(offset),
            'stacktrace': 'Drift is {} seconds'.format(response.offset)
        }
    else:
        result = {'ok': True}

    return {'clock sync': result}
