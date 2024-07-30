import copy
import datetime
import os
import sys
import unittest
from datetime import date, timedelta
from unittest import mock

import requests
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

from retirement_api.utils.ss_calculator import (
    calculate_lifetime_benefits,
    clean_comment,
    get_retire_data,
    interpolate_benefits,
    interpolate_for_past_fra,
    num_test,
    parse_details,
    parse_response,
    set_up_runvars,
    validate_date,
)
from retirement_api.utils.ss_utilities import (
    age_map,
    get_current_age,
    get_delay_bonus,
    get_months_past_birthday,
    get_months_until_next_birthday,
    get_retirement_age,
    past_fra_test,
    yob_test,
)


# ,
#                          run_tests)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


class UtilitiesTests(unittest.TestCase):
    today = datetime.date.today()
    # in case this test happens to run on a leap day; and yes, this happened
    if today.day == 29 and today.month == 2:  # pragma: no cover
        today = today.replace(day=today.day - 1)

    sample_year = today.year - 61

    sample_params = {
        "dobmon": 1,
        "dobday": 5,
        "yob": sample_year,
        "earnings": 70000,
        "lastYearEarn": "",
        "lastEarn": "",
        "retiremonth": 1,
        "retireyear": 2037,
        "dollars": 1,
        "prgf": 2,
    }
    sample_results = {
        "data": {
            "early retirement age": "",
            "full retirement age": "",
            "benefits": {
                "age 62": 0,
                "age 63": 0,
                "age 64": 0,
                "age 65": 0,
                "age 66": 0,
                "age 67": 2176,
                "age 68": 0,
                "age 69": 0,
                "age 70": 0,
            },
            "params": {
                "dobmon": 1,
                "dobday": 5,
                "yob": sample_year,
                "earnings": 40000,
                "lastYearEarn": "",
                "lastEarn": "",
                "retiremonth": 1,
                "retireyear": 2037,
                "dollars": 1,
                "prgf": 2,
            },
            "disability": "",
            "months_past_birthday": 0,
            "survivor benefits": {
                "child": "",
                "spouse caring for child": "",
                "spouse at full retirement age": "",
                "family maximum": "",
            },
        },
        "current_age": 44,
        "error": "",
        "note": "",
        "past_fra": False,
    }

    sample_lifetime_benefits = {
        "age62": 261800,  # born in 1957, 40K
        "age63": 267168,
        "age64": 274176,
        "age65": 282000,
        "age66": 289932,
        "age67": 293328,
        "age68": 298248,
        "age69": 300672,
        "age70": 300600,
    }

    data_keys = [
        "early retirement age",
        "full retirement age",
        "lifetime",
        "benefits",
        "params",
        "disability",
        "months_past_birthday",
        "survivor benefits",
    ]
    benefit_keys = [
        "age 62",
        "age 63",
        "age 64",
        "age 65",
        "age 66",
        "age 67",
        "age 68",
        "age 69",
        "age 70",
    ]

    def test_calculate_lifetime_benefits(self):
        results = copy.deepcopy(self.sample_results)
        results["data"]["benefits"] = {
            "age 62": 952,
            "age 63": 1012,
            "age 64": 1088,
            "age 65": 1175,
            "age 66": 1306,
            "age 67": 1358,
            "age 68": 1462,
            "age 69": 1566,
            "age 70": 1670,
        }
        results["current_age"] = 59
        base_benefit = 1306
        fra_tuple = (66, 6)
        dob = datetime.date(self.sample_year - 13, 1, 3)
        past_fra = False
        test_results = calculate_lifetime_benefits(
            results, base_benefit, fra_tuple, dob, past_fra
        )
        for key in results["data"]["benefits"]:
            lifekey = key.replace("age ", "age")
            self.assertTrue(
                self.sample_lifetime_benefits[lifekey]
                == test_results["data"]["lifetime"][lifekey]
            )
        dob = dob.replace(day=2)
        test_results = calculate_lifetime_benefits(
            results, base_benefit, fra_tuple, dob, past_fra
        )
        self.assertTrue(test_results["data"]["lifetime"]["age62"] == 262752)

    def test_clean_comment(self):
        test_comment = "<!-- This is a test comment    -->"
        expected_comment = "This is a test comment"
        self.assertTrue(clean_comment(test_comment) == expected_comment)

    def test_set_up_runvars(self):
        mock_params = copy.copy(self.sample_params)
        (
            test_dob,
            test_dobstring,
            test_current_age,
            test_fra_tuple,
            test_past_fra,
            test_results,
        ) = set_up_runvars(mock_params)
        self.assertTrue(
            test_results["data"]["params"]["yob"] == self.sample_year
        )
        mock_params["dobday"] = 1
        (
            test_dob,
            test_dobstring,
            test_current_age,
            test_fra_tuple,
            test_past_fra,
            test_results2,
        ) = set_up_runvars(mock_params)
        self.assertTrue(
            test_results2["data"]["params"]["yob"] == self.sample_year - 1
        )

    def test_months_past_birthday(self):
        dob = self.today - timedelta(days=(365 * 20) + 6)
        self.assertTrue(get_months_past_birthday(dob) in [0, 1])
        dob = self.today - timedelta(days=(365 * 20) + 70)
        self.assertTrue(get_months_past_birthday(dob) in [2, 3])
        dob = self.today - timedelta(days=(365 * 20) + 320)
        self.assertTrue(get_months_past_birthday(dob) in [10, 11])

    def test_months_until_next_bday(self):
        age40 = self.today.replace(year=(self.today.year - 40))
        bd_two_days_later = age40 + datetime.timedelta(days=2)
        bd_month_later = age40 + datetime.timedelta(days=30)
        diff1 = get_months_until_next_birthday(age40)
        diff2 = get_months_until_next_birthday(bd_two_days_later)
        diff3 = get_months_until_next_birthday(bd_month_later)
        self.assertTrue(diff1 == 12)
        self.assertTrue(diff2 in [0, 1])
        self.assertTrue(diff3 in [1, 2])

    def test_get_current_age(self):
        for birthday, today, expected_age in [
            ("1-1-1964", "1-1-2024", 60),
            ("1-1-1964", "12-31-2023", 59),
            ("2-29-1980", "1-29-2015", 34),
            ("2-29-2024", "3-1-2124", 100),
            ("2-29-2024", "2-29-2124", 100),
            ("2-29-2024", "2-28-2124", 99),
            ("2-29-2024", "2-28-2025", 0),
            ("2-29-2024", "3-1-2025", 1),
            ("6-1-2020", "5-31-2020", None),
            ("6-1-2020", "6-1-2020", 0),
            ("6-1-2020", "5-31-2021", 0),
            ("6-1-2020", "6-1-2021", 1),
            ("xx", "12-31-2024", None),
        ]:
            with self.subTest(
                birthday=birthday, today=today, expected_age=expected_age
            ), freeze_time(today):
                self.assertEqual(get_current_age(birthday), expected_age)

    def test_interpolate_benefits(self):
        mock_results = copy.deepcopy(self.sample_results)
        expected_benefits = {
            "age 62": 1532,
            "age 63": 1632,
            "age 64": 1741,
            "age 65": 1886,
            "age 66": 2031,
            "age 67": 2176,
            "age 68": 2350,
            "age 69": 2524,
            "age 70": 2698,
        }
        dob = self.today.replace(year=self.today.year - 44)
        if dob.day == 2:  # pragma: no cover
            expected_benefits["age 62"] = 1523
        # need to pass results, base, fra_tuple, current_age, DOB
        results = interpolate_benefits(mock_results, 2176, (67, 0), 44, dob)
        for key in results["data"]["benefits"]:
            self.assertTrue(
                results["data"]["benefits"][key] == expected_benefits[key]
            )
        mock_results["data"]["benefits"]["age 66"] = mock_results["data"][
            "benefits"
        ]["age 67"]
        mock_results["data"]["benefits"]["age 67"] = 0
        dob = (
            self.today
            - datetime.timedelta(days=365 * 55)
            - datetime.timedelta(days=14)
        )
        results = interpolate_benefits(mock_results, 2176, (66, 0), 55, dob)
        for key in sorted(results["data"]["benefits"].keys()):
            self.assertTrue(results["data"]["benefits"][key] != 0)
        dob = dob.replace(day=2)
        results = interpolate_benefits(mock_results, 2176, (66, 0), 55, dob)
        self.assertTrue(results["data"]["benefits"]["age 62"] != 0)
        dob = dob.replace(year=self.today.year - 45)
        results = interpolate_benefits(mock_results, 2176, (67, 0), 45, dob)
        self.assertTrue(results["data"]["benefits"]["age 62"] != 0)
        dob = self.today - datetime.timedelta(days=365 * 64)
        results = interpolate_benefits(mock_results, 2176, (66, 0), 64, dob)
        for key in sorted(results["data"]["benefits"].keys())[2:]:
            self.assertTrue(results["data"]["benefits"][key] != 0)
        dob = self.today - datetime.timedelta(days=365 * 65)
        results = interpolate_benefits(mock_results, 2176, (66, 0), 65, dob)
        for key in sorted(results["data"]["benefits"].keys())[3:]:
            self.assertTrue(results["data"]["benefits"][key] != 0)
        dob = self.today - datetime.timedelta(days=365 * 63)
        results = interpolate_benefits(mock_results, 2176, (66, 0), 63, dob)
        for key in sorted(results["data"]["benefits"].keys())[1:]:
            self.assertTrue(results["data"]["benefits"][key] != 0)

    def test_parse_details(self):
        sample_rows = [
            "early: Base year for indexing is 2013. "
            "Bend points are 826 & 4980",
            "AIME = 2930 & PIA in 2018 is 1416.6.",
            "PIA in 2018 after COLAs is $1,416.60.",
        ]
        output = {
            "EARLY": {
                "AIME": "AIME = 2930 & PIA in 2018 is 1416.6.",
                "Bend points": "Base year for indexing is 2013. "
                "Bend points are 826 & 4980",
                "COLA": "PIA in 2018 after COLAs is $1,416.60.",
            }
        }
        self.assertEqual(parse_details(sample_rows), output)

    def test_parse_response(self):
        result = parse_response({}, "", "en")
        self.assertTrue(result[1] == 0)
        self.assertTrue("error" in result[0])
        self.assertTrue("responding" in result[0]["note"])
        result = parse_response({}, "", "es")
        self.assertTrue("error" in result[0])
        self.assertTrue("respondiendo" in result[0]["note"])
        self.assertTrue(result[1] == 0)

    def check_interpolate_for_past_fra(
        self, today, dob, base_benefit, expected_benefits
    ):
        """Tests benefits of retirees past full retirement age."""
        mock_results = {"data": {"benefits": {}}}

        # current_age = relativedelta(today, dob).years

        with freeze_time(today):
            results = interpolate_for_past_fra(
                results=mock_results,
                base=base_benefit,
                current_age=relativedelta(today, dob).years,
                dob=dob,
            )

        self.assertEqual(results["data"]["benefits"], expected_benefits)

    def test_interpolate_for_past_fra_68(self):
        self.check_interpolate_for_past_fra(
            today=date(2018, 6, 15),
            dob=date(1949, 12, 15),
            base_benefit=1431,
            expected_benefits={
                # Benefit at current age should equal base benefit.
                "age 68": 1431,
                # Turning 69 in 6 months. Waiting to retire until age 69
                # should equal base benefit plus a bump equal to 6 * .667%.
                # 1431 * (1 + (.00667 * 6)) =  1488
                "age 69": 1488,
                # Turning 70 in one year plus six months. Waiting to retire
                # until then adds another 8% of base benefit.
                # 1431 * (1 + (.00667 * 6) + (.08)) = 1602
                "age 70": 1602,
            },
        )

    def test_interpolate_for_past_fra_68_born_on_the_1st_next_month(self):
        # Per ssa.gov, "if your birthday is on the 1st of the month, we
        # compute your benefit as if your birthday were in the previous month."
        # https://www.ssa.gov/planners/retire/1943-delay.html
        #
        # Calculator thus treats someone turning 69 on the 1st next month
        # as if they were turning 69 this month, i.e that there are no months
        # left until they are 69. So "current age" is treated as 69.
        self.check_interpolate_for_past_fra(
            today=date(2018, 5, 15),
            dob=date(1949, 6, 1),
            base_benefit=1431,
            expected_benefits={
                # Benefit at "current age" should equal base benefit.
                "age 69": 1431,
                # Turning 70 in one year. Waiting to retire until then adds
                # another 8% of base benefit.
                # 1431 * (1 + .08) = 1545
                "age 70": 1545,
            },
        )

    def test_validate_date_invalid(self):
        test_params = {"yob": 1952, "dobmon": 2, "dobday": 30}
        validate = validate_date(test_params)
        self.assertIs(validate, False)

    def test_validate_date_valid(self):
        test_params = {"yob": 1952, "dobmon": 2, "dobday": 29}
        validate = validate_date(test_params)
        self.assertIs(validate, True)

    def test_num_test(self):
        inputs = [
            ("", False),
            ("a", False),
            ("3c", False),
            ("4", True),
            (4, True),
            (4.4, True),
            ("55.0", True),
            ("0.55", True),
        ]
        for tup in inputs:
            self.assertEqual(num_test(tup[0]), tup[1])

    def test_get_retirement_age(self):
        """
        given a worker's birth year,
        should return full retirement age in years and months
        """
        sample_inputs = {
            "1920": (65, 0),
            "1937": (65, 0),
            "1938": (65, 2),
            "1939": (65, 4),
            "1940": (65, 6),
            "1941": (65, 8),
            "1942": (65, 10),
            "1943": (66, 0),
            "1945": (66, 0),
            "1954": (66, 0),
            "1955": (66, 2),
            "1956": (66, 4),
            "1957": (66, 6),
            "1958": (66, 8),
            "1959": (66, 10),
            "1960": (67, 0),
            "1980": (67, 0),
            "198": None,
            "abc": None,
            str(self.today.year + 1): None,
        }
        for year in sample_inputs:
            self.assertEqual(get_retirement_age(year), sample_inputs[year])

    def test_past_fra_test(self):
        one_one = f"{date(1980, 1, 1).replace(year=self.today.year - 25)}"
        way_old = f"{self.today - timedelta(days=80 * 365)}"
        too_old = f"{self.today - timedelta(days=68 * 365)}"
        ok = f"{self.today - timedelta(days=57 * 365)}"
        too_young = f"{self.today - timedelta(days=21 * 365)}"
        future = f"{self.today + timedelta(days=365)}"
        # edge = "{0}".format(self.today - timedelta(days=67 * 365))
        invalid = "xx/xx/xxxx"
        self.assertFalse(past_fra_test(one_one, language="en"))
        self.assertTrue(past_fra_test(too_old, language="en"))
        self.assertTrue(past_fra_test(too_old, language="es"))
        self.assertFalse(past_fra_test(ok, language="en"))
        self.assertTrue("22" in past_fra_test(too_young, language="en"))
        self.assertTrue("sentimos" in past_fra_test(too_young, language="es"))
        self.assertTrue("22" in past_fra_test(future, language="en"))
        self.assertTrue("70" in past_fra_test(way_old, language="en"))
        # self.assertTrue(past_fra_test(edge, language="en"))
        self.assertTrue("invalid" in past_fra_test(invalid, language="en"))
        self.assertTrue("invalid" in past_fra_test())

    def test_age_map(self):
        self.assertTrue(isinstance(age_map, dict))
        for year in age_map:
            self.assertTrue(isinstance(age_map[year], tuple))

    def test_get_delay_bonus(self):
        sample_inputs = {
            "1933": 5.5,
            "1934": 5.5,
            "1935": 6.0,
            "1937": 6.5,
            "1939": 7.0,
            "1941": 7.5,
            "1943": 8.0,
            "1953": 8.0,
            "1963": 8.0,
            "1973": 8.0,
            "1983": 8.0,
            "1922": None,
        }
        for year in sample_inputs:
            self.assertEqual(get_delay_bonus(year), sample_inputs[year])

    def test_yob_test(self):
        sample_inputs = {
            "1933": "1933",
            str(self.today.year + 2): None,
            "935": None,
            "1957": "1957",
            "1979": "1979",
            "abc": None,
            1980: "1980",
            None: None,
        }
        for year in sample_inputs:
            self.assertEqual(yob_test(year), sample_inputs[year])

    """
    ## sample params: ##
            'dobmon': 8,
            'dobday': 14,
            'yob': 1956,
            'earnings': 50000,

    ## sample results: ##
        results = {'data': {
                        'early retirement age': '',
                        u'full retirement age': '',
                        'benefits': {
                            'age 62': 0,
                            'age 63': 0,
                            'age 64': 0,
                            'age 65': 0,
                            'age 66': 0,
                            'age 67': 0,
                            'age 68': 0,
                            'age 69': 0,
                            'age 70': 0
                            }
                        'params': params,
                        'disability': '',
                        'survivor benefits': {
                                        'child': '',
                                        'spouse caring for child': '',
                                        'spouse at full retirement age': '',
                                        'family maximum': ''
                                        }
                        }
                  }
    """

    @mock.patch("retirement_api.utils.ss_calculator.requests.post")
    def _get_retire_data(
        self,
        mock_request_post,
        response_text=None,
        param_overrides=None,
    ):
        """given a birth date and annual pay value,
        return a dictionary of social security values
        """
        if response_text is None:
            response_text = """<div>
                $<span id="ret_amount">2,035.00</span>
            </div>"""
        mock_request_post.return_value.text = response_text

        params = copy.copy(self.sample_params)
        if param_overrides is not None:
            params.update(param_overrides)

        results = get_retire_data(params, language="en")
        return results

    def test_get_retire_data_base_sample(self):
        data = self._get_retire_data()["data"]
        self.assertEqual(data["params"]["yob"], self.sample_year)

        for each in data:
            self.assertTrue(each in self.data_keys)
        for each in data["benefits"]:
            self.assertTrue(each in self.benefit_keys)

    def test_get_retire_data_too_young(self):
        params = {}
        params["yob"] = self.today.year - 21
        results = self._get_retire_data(param_overrides=params)
        self.assertTrue("22" in results["note"])

    def test_get_retire_data_too_old(self):
        params = {}
        too_old_birthday = self.today - relativedelta(years=71, days=1)
        params["dobmon"] = too_old_birthday.month
        params["dobday"] = too_old_birthday.day
        params["yob"] = too_old_birthday.year
        results = self._get_retire_data(param_overrides=params)
        self.assertTrue("older than 70" in results["note"])

    def test_get_retire_data_insufficient_earnings(self):
        params = {}
        params["earnings"] = 0
        response_text = """<p>0 is insufficient to receive benefits.</p>"""
        data = self._get_retire_data(
            response_text=response_text, param_overrides=params
        )
        self.assertTrue("zero" in data["error"])

    @mock.patch("retirement_api.utils.ss_calculator.requests.post")
    def test_bad_calculator_requests(self, mock_requests):
        params = copy.copy(self.sample_params)
        mock_requests.return_value.ok = False
        mock_results = get_retire_data(params, language="en")
        self.assertTrue("not responding" in mock_results["error"])
        mock_requests.side_effect = requests.exceptions.RequestException
        mock_results = get_retire_data(params, language="en")
        self.assertTrue("request error" in mock_results["error"])
        mock_results = get_retire_data(params, language="es")
        self.assertTrue("request error" in mock_results["error"])
        mock_requests.side_effect = requests.exceptions.ConnectionError
        mock_results = get_retire_data(params, language="en")
        self.assertTrue("connection error" in mock_results["error"])
        mock_requests.side_effect = requests.exceptions.Timeout
        mock_results = get_retire_data(params, language="en")
        self.assertTrue("timed out" in mock_results["error"])
        mock_requests.side_effect = ValueError
        mock_results = get_retire_data(params, language="en")
        self.assertTrue("SSA" in mock_results["error"])
