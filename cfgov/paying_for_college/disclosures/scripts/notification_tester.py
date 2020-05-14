import datetime

import requests

from paying_for_college.models import Contact


# urls
EDMC_DEV = "https://dev.exml.edmc.edu/cfpb"
EDMC_BETA = "https://beta.exml.edmc.edu/cfpb"
EDMC_PROD = 'edmc'
BPI_PROD = 'bpi'
BIN = "https://httpbin.org/"
BINPOST = "https://httpbin.org/post"
BINGET = "https://httpbin.org/get"

# test values
OID = '9e0280139f3238cbc9702c7b0d62e5c238a835d0'
ERRORS = 'INVALID: test notification via Python'
REPORT = ('URL is {}\nOK is {}\nReason is {}\n'
          'Status is {}\nTime sent is {}\nHeaders are {}\n'
          'Origin is {}')


def send_test_notification(url, oid, errors):
    """
    Send fake notifiations to various endpoints to help troubleshoot.

    You can send a test notification to a school's endpoint to confirm
    reception, or send to httpbin to check the outbound IP (origin),
    headers, and the data payload.
    Examples:
    - print(send_test_notification(EDMC_PROD, OID, ERRORS))
    - print(send_test_notification(BPI_PROD, OID, ERRORS))
    - print(send_test_notification(BINPOST, OID, ERRORS))
    """
    prod_endpoints = {
        'edmc': Contact.objects.get(name='EDMC').endpoint,
        'bpi': Contact.objects.get(name='Bridgepoint Education').endpoint
    }
    if url in prod_endpoints:
        _url = prod_endpoints[url]
    else:
        _url = url
    payload = {
        'oid': oid,
        'time': "{0}+00:00".format(datetime.datetime.now().isoformat()),
        'errors': errors
    }
    try:
        resp = requests.post(_url, data=payload, timeout=10)
    except requests.exceptions.ConnectTimeout:
        return "post to {} timed out".format(url)
    if not resp.content:
        print("Got a blank response from {}".format(url))
        return
    json_content = resp.json()
    report = REPORT.format(
        url,
        resp.ok,
        resp.reason,
        resp.status_code,
        payload['time'],
        json_content.get('headers'),
        json_content.get('origin')
    )
    return report

# curl test example:
# curl -v -X POST --data "oid=f38283b5b7c939a058889f997949efa566c616c5&errors=INVALID: test notification via curl&time=2016-01-21T18:36:09.922690+00:00" --url "https://dev.exml.edmc.edu/cfpb"  # noqa
