# send test notifications to school
import datetime

import requests


# urls
EDMC_DEV = "https://dev.exml.edmc.edu/cfpb"
EDMC_BETA = "https://beta.exml.edmc.edu/cfpb"
EDMC_PROD = "https://exml.edmc.edu/cfpb"
BIN = "https://httpbin.org/"
BINPOST = "https://httpbin.org/post"
BINGET = "https://httpbin.org/get"
RBIN = "http://requestb.in/{}"

# test values
OID = '9e0280139f3238cbc9702c7b0d62e5c238a835d0'
ERRORS = 'INVALID: test notification via Python'
REPORT = ('URL is {}; OK is {}; reason is {}; '
          'status is {}; time sent is {};\n content is {}\n')


def notify_edmc(url, oid, errors):
    payload = {
        'oid': oid,
        'time': "{0}+00:00".format(datetime.datetime.now().isoformat()),
        'errors': errors
    }
    try:
        resp = requests.post(url, data=payload, timeout=10)
    except requests.exceptions.ConnectTimeout:
        return "post to {0} timed out".format(url)
    report = REPORT.format(url,
                           resp.ok,
                           resp.reason,
                           resp.status_code,
                           payload['time'],
                           resp.content)
    return report


if __name__ == "__main__":  # pragma: no cover
    print(notify_edmc(EDMC_DEV, OID, ERRORS))
    print(notify_edmc(EDMC_BETA, OID, ERRORS))
    print(notify_edmc(EDMC_PROD, OID, ERRORS))

# to test against binpost
# hit_binpost = requests.post(BINPOST, data=PAYLOAD)
# print hit_binpost.content

# to hit rbin
# hit_rbin = requests.post(RBIN, data=PAYLOAD)
# then check http://requestb.in/1ak4sxc1?inspect#s8ubhf

# curl test
# curl -v -X POST --data "oid=f38283b5b7c939a058889f997949efa566c616c5&errors=INVALID: test notification via curl&time=2016-01-21T18:36:09.922690+00:00" --url "https://dev.exml.edmc.edu/cfpb"  # noqa
