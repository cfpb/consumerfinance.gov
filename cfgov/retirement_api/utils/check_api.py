# script to check the retirement api to make sure
# the SSA Quick Calculator is operational
# and to log the result to a csv
import datetime
import json
import logging
import os
import random
import signal
import sys
import time

import requests


timestamp = datetime.datetime.now()
default_base = "build"

# rolling dob to guarantee subject is 44 and full retirement age is 67
dob = timestamp.date().replace(year=timestamp.year - 44)
timeout_seconds = 20

API_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class TimeoutError(Exception):
    pass


def handler(signum, frame):
    raise TimeoutError("Request timed out")


class Collector:
    data = ""
    date = ("{0}".format(timestamp))[:16]
    domain = ""
    status = ""
    error = ""
    note = ""
    api_fail = ""
    timer = ""


collector = Collector()

log_header = ["data", "date", "domain", "status", "error", "api_fail", "timer"]


def build_msg(collector):
    msg = ",".join([collector.__getattribute__(key) for key in log_header])
    return msg


def check_data(data):
    """For a 44-year-old, the api should
    always return an age, a full retirement age
    and a value for benefits at age 70
    """
    if (
        data["current_age"] == 44
        and data["data"]["full retirement age"] == "67"
        and data["data"]["benefits"]["age 70"]
    ):
        return "OK"
    else:
        return "BAD DATA"


prefix = "http://"
suffix = ".consumerfinance.gov/retirement"
api_string = "retirement-api/estimator/{0}-{1}-{2}/{3}/".format(
    dob.month, dob.day, dob.year, random.randrange(20000, 100000)
)
BASES = {
    "unitybox": "http://localhost:8080/retirement",
    "standalone": "http://localhost:8000/retirement",
    default_base: "{0}{1}{2}".format(prefix, default_base, suffix),
    "prod": "{0}www{1}".format(prefix, suffix),
}


def run(base):
    if base not in BASES:
        collector.error = "Server '{0}' isn't recognized".format(base)
        return collector
    url = "{0}/{1}".format(BASES[base], api_string)
    collector.domain = base
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_seconds)
    start = time.time()
    # print "trying request at {0}".format(url)
    try:
        test_request = requests.get(url)
    except requests.ConnectionError:
        end = time.time()
        signal.alarm(0)
        collector.status = "ABORTED"
        collector.error = "Server connection error"
        collector.api_fail = "FAIL"
    except TimeoutError:
        end = time.time()
        signal.alarm(0)
        collector.status = "TIMEDOUT"
        collector.error = "SSA request exceeded {0} sec".format(
            timeout_seconds
        )
    else:
        if test_request.status_code != 200:
            signal.alarm(0)
            end = time.time()
            collector.status = "{0}".format(test_request.status_code)
            collector.error = test_request.reason.replace(",", ";")
            collector.api_fail = "FAIL"
        else:
            end = time.time()
            signal.alarm(0)
            data = json.loads(test_request.text)
            collector.status = "%s" % test_request.status_code
            collector.error = (
                "{0}".format(data["error"])
                .replace(",", ";")
                .replace("'", "")
                .replace('"', "")
            )
            collector.note = data["note"]
            collector.data = check_data(data)
            if collector.data == "BAD DATA":
                collector.api_fail = "FAIL"
    collector.timer = "%s" % round(end - start, 1)
    build_msg(collector)
    # print msg
    # with open('%s/tests/logs/api_check.log' % API_ROOT, 'a') as f:
    #     f.write("%s\n" % msg)
    return collector


if __name__ == "__main__":
    """
    runs against one of these base urls:
    unitybox, standalone, build, or prod;
    defaults to build
    """
    helpmsg = "pass a base to test: unitybox, standalone, build, or prod"
    try:
        BASE = sys.argv[1]
    except Exception:
        run(default_base)
    else:
        if BASE in BASES:
            run(BASE)
        else:
            logging.getLogger(__name__).info(helpmsg)
            sys.exit()
