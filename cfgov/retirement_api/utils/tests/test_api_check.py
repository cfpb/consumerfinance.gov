import datetime
import json
import unittest

import mock
import requests

from ..check_api import Collector, TimeoutError, build_msg, check_data, run

timestamp = datetime.datetime.now()


class TestApi(unittest.TestCase):
    """test the tester"""

    test_collector = Collector()
    test_collector.domain = "build"
    test_data = {
        "current_age": 44,
        "note": "",
        "data": {
            "benefits": {
                "age 63": 1603,
                "age 62": 1476,
                "age 67": 2137,
                "age 66": 1995,
                "age 65": 1852,
                "age 64": 1710,
                "age 69": 2479,
                "age 68": 2308,
                "age 70": 2650,
            },
            "disability": "$1,899",
            "early retirement age": "62 and 1 month",
            "params": {
                "dollars": 1,
                "lastYearEarn": "",
                "dobday": 7,
                "prgf": 2,
                "dobmon": 7,
                "retiremonth": "",
                "retireyear": "",
                "yob": 1970,
                "lastEarn": "",
                "earnings": 70000,
            },
            "full retirement age": "67",
            "survivor benefits": {
                "spouse at full retirement age": "$1,912",
                "family maximum": "$3,377",
                "spouse caring for child": "$1,434",
                "child": "$1,434",
            },
        },
        "error": "",
    }

    def test_check_data(self):
        msg = check_data(self.test_data)
        self.assertTrue(msg == "OK")

    def test_build_msg(self):
        target_text = ",{0},build,,,,".format(self.test_collector.date)
        test_text = build_msg(self.test_collector)
        self.assertTrue(test_text == target_text)

    @mock.patch("retirement_api.utils.check_api.requests.get")
    @mock.patch("retirement_api.utils.check_api.build_msg")
    def test_run(self, mock_build_msg, mock_requests):
        mock_requests.return_value.text = json.dumps(self.test_data)
        mock_requests.return_value.status_code = 200
        mock_build_msg.return_value = (
            ",%s,,,mock error,,," % self.test_collector.date
        )
        run("build")
        self.assertTrue(mock_build_msg.call_count == 1)
        mock_requests.return_value.status_code = 400
        collector = run("build")
        self.assertTrue("FAIL" in collector.api_fail)
        collector = run("fakeplaceholder.com")
        self.assertTrue("recognized" in collector.error)
        mock_requests.side_effect = requests.ConnectionError
        collector = run("build")
        self.assertTrue(collector.status == "ABORTED")
        mock_requests.side_effect = TimeoutError
        collector = run("prod")
        self.assertTrue(collector.status == "TIMEDOUT")
