import datetime
import json

# import unittest
from django.http import HttpRequest
from django.test import TestCase

from retirement_api.views import (
    estimator,
    get_full_retirement_age,
    income_check,
    param_check,
)


try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


today = datetime.datetime.now().date()

PARAMS = {
    "dobmon": 8,
    "dobday": 14,
    "yob": 1970,
    "earnings": 70000,
    "lastYearEarn": "",  # possible use for unemployed or already retired
    "lastEarn": "",  # possible use for unemployed or already retired
    "retiremonth": "",  # leve blank to get triple calculation -- 62, 67 and 70
    "retireyear": "",  # leve blank to get triple calculation -- 62, 67 and 70
    "dollars": 1,  # benefits to be calculated in current-year dollars
    "prgf": 2,
}


class ViewTests(TestCase):
    fixtures = ["retiredata.json"]

    req_good = HttpRequest()
    req_good.GET["dob"] = "1955-05-05"
    req_good.GET["income"] = "40000"
    req_blank = HttpRequest()
    req_blank.GET["dob"] = ""
    req_blank.GET["income"] = ""
    req_invalid = HttpRequest()
    req_invalid.GET["dob"] = "1-2-%s" % (today.year + 5)
    req_invalid.GET["income"] = "x"
    return_keys = ["data", "error"]

    def test_base_view(self):
        url = reverse("retirement_api:claiming")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)
        url = reverse("retirement_api:claiming_es")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)

    def test_param_check(self):
        self.assertEqual(param_check(self.req_good, "dob"), "1955-05-05")
        self.assertEqual(param_check(self.req_good, "income"), "40000")
        self.assertEqual(param_check(self.req_blank, "dob"), None)
        self.assertEqual(param_check(self.req_blank, "income"), None)

    def test_income_check(self):
        self.assertEqual(income_check("544.30"), 544)
        self.assertEqual(income_check("$55,000.15"), 55000)
        self.assertEqual(income_check("0"), 0)
        self.assertEqual(income_check("x"), None)
        self.assertEqual(income_check(""), None)

    def test_get_full_retirement_age(self):
        request = self.req_blank
        response = get_full_retirement_age(request, birth_year="1953")
        self.assertTrue(json.loads(response.content) == [66, 0])
        response2 = get_full_retirement_age(request, birth_year=1957)
        self.assertTrue(json.loads(response2.content) == [66, 6])
        response3 = get_full_retirement_age(request, birth_year=1969)
        self.assertTrue(json.loads(response3.content) == [67, 0])
        response4 = get_full_retirement_age(request, birth_year=969)
        self.assertTrue(response4.status_code == 400)

    def test_estimator_url_data(self):
        request = self.req_blank
        response = estimator(request, dob="1955-05-05", income="40000")
        self.assertIsInstance(response.content, bytes)
        rdata = json.loads(response.content)
        for each in self.return_keys:
            self.assertTrue(each in rdata.keys())

    def test_estimator_url_data_bad_income(self):
        request = self.req_blank
        response = estimator(request, dob="1955-05-05", income="z")
        self.assertTrue(response.status_code == 400)

    def test_estimator_url_data_bad_dob(self):
        request = self.req_blank
        response = estimator(request, dob="1955-05-xx", income="4000")
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data(self):
        request = self.req_good
        response = estimator(request)
        self.assertTrue(response.status_code == 200)
        self.assertIsInstance(response.content, bytes)
        rdata = json.loads(response.content)
        for each in self.return_keys:
            self.assertTrue(each in rdata.keys())

    def test_estimator_query_data_blank(self):
        request = self.req_blank
        response = estimator(request)
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data_blank_dob(self):
        request = self.req_blank
        response = estimator(request, income="40000")
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data_blank_income(self):
        request = self.req_blank
        response = estimator(request, dob="1955-05-05")
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data_bad_income(self):
        request = self.req_invalid
        response = estimator(request, dob="1955-05-05")
        self.assertTrue(response.status_code == 400)

    def test_about_pages(self):
        url = reverse("retirement_api:about")
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)
        url = reverse("retirement_api:about_es", kwargs={"language": "es"})
        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)
