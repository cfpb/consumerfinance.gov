import datetime

import requests

from paying_for_college.models import Contact


# urls
BIN = "https://httpbin.org/"
BINPOST = "https://httpbin.org/post"
BINGET = "https://httpbin.org/get"

# test values
OID = '9e0280139f3238cbc9702c7b0d62e5c238a835d0'
ERRORS = 'INVALID: test notification via Python'
REPORT = ('URL is {}\nOK is {}\nReason is {}\n'
          'Status is {}\nTime sent is {}')


def send_test_notifications(url=None, oid=OID, errors=ERRORS):
    """
    Send fake notifications to school endpoints to help troubleshoot.

    You can send test notifications to school endpoints to confirm
    reception, or send to httpbin to check the outbound IP (origin),
    headers, and the data payload.
    Examples:
    - print(send_test_notifications())
    - print(send_test_notifications(url=BINPOST))
    """
    prod_endpoints = {
        # 'edmc': Contact.objects.get(name='EDMC').endpoint,
        'bpi': Contact.objects.get(name='Bridgepoint Education').endpoint,
        'su': Contact.objects.get(name='South University').endpoint,
        'ai': Contact.objects.get(name='Art Institutes').endpoint,
    }
    if not url:
        urls = list(prod_endpoints.values())
    else:
        urls = [url]
    payload = {
        'oid': oid,
        'time': f"{datetime.datetime.now().isoformat()}+00:00",  # noqa
        'errors': errors
    }
    msg = ""
    for _url in urls:
        try:
            resp = requests.post(_url, data=payload, timeout=10)
        except requests.exceptions.ConnectTimeout:
            msg += f"Post to {_url} timed out.\n"
        else:
            report = REPORT.format(
                _url,
                resp.ok,
                resp.reason,
                resp.status_code,
                payload['time'],
            )
            msg += f"{report}\n"
            if resp.content:
                msg += f"Response content: {resp.content}\n"
    return msg


# curl_examples
"""
curl -v https://httpbin.org/get
curl -v -X POST https://httpbin.org/post

export XDATA="oid='f38283b5b7c939a058889f997949efa566c616c5'&errors='INVALID: test notification via curl'&time='2020-06-24T18:36:09.922690+00:00'"  # noqa
export BPI="https://sissecureservices.bpiedu.com/routingmanager/api/cfpb"
export EDMC="https://exml.dcedh.org/cfpb"

curl -v --data "$XDATA" --url "$BPI"
curl -v --data "$XDATA" --url "$EDMC"
"""
