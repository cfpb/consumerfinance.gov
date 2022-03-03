import csv
import datetime
import json
import os
import shutil
import sys
import tempfile

from django.test import TestCase

import mock
from bs4 import BeautifulSoup as bs
from retirement_api import utils
from retirement_api.utils.ss_update_stats import (
    make_soup,
    output_csv,
    output_json,
)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


TODAY = datetime.date.today()
mock_data_path = "{0}/retirement_api/data/mock_data".format(BASE_DIR)


class UpdateSsStatsTests(TestCase):
    cola_page = "{0}/ssa_cola.html".format(mock_data_path)
    awi_page = "{0}/ssa_awi_series.html".format(mock_data_path)
    life_page = "{0}/ssa_life.html".format(mock_data_path)
    earlyretire_page = "{0}/ssa_earlyretire.html".format(mock_data_path)
    life_headings = [
        "exact_age",
        "male_death_probability",
        "male_number_of_lives",
        "male_life_expectancy",
        "female_death_probability",
        "female_number_of_lives",
        "female_life_expectancy",
    ]
    sample_life_results = {
        1: "0,0.006680,100000,76.10,0.005562,100000,80.94",
        10: "9,0.000096,99164,67.74,0.000090,99313,72.50",
        100: "99,0.339972,1323,2.22,0.287178,3807,2.60",
    }

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    # def output_csv(filepath, headings, bs_rows):
    def test_output_csv(self):
        """outputs csv based on inputs of
        headings and beautiful_soup rows
        """
        mockpath = "{0}/mock_life.csv".format(self.tempdir)
        with open(self.life_page, "r") as f:
            mockpage = f.read()
        table = bs(mockpage, "html.parser").find("table").find("table")
        rows = table.findAll("tr")[2:]
        output_csv(mockpath, self.life_headings, rows)
        self.assertTrue(os.path.isfile(mockpath))
        with open(mockpath, "r") as f:
            reader = csv.reader(f)
            data = [row for row in reader]
        for sample in self.sample_life_results:
            self.assertEqual(
                data[sample], self.sample_life_results[sample].split(",")
            )

    # def output_json(filepath, headings, bs_rows):
    def test_output_json(self):
        """outputs json to file based on inputs of
        path, headings and beautiful_soup rows
        """
        mockpath = "{0}/mock_life.json".format(self.tempdir)
        sample_json_results = {
            "0": {
                "female_life_expectancy": "80.94",
                "male_life_expectancy": "76.10",
            },
            "57": {
                "female_life_expectancy": "26.91",
                "male_life_expectancy": "23.69",
            },
            "99": {
                "female_life_expectancy": "2.60",
                "male_life_expectancy": "2.22",
            },
        }
        with open(self.life_page, "r") as f:
            mockpage = f.read()
        table = bs(mockpage, "html.parser").find("table").find("table")
        rows = table.findAll("tr")[2:]
        output_json(mockpath, self.life_headings, rows)
        self.assertTrue(os.path.isfile(mockpath))
        with open(mockpath, "r") as f:
            data = json.loads(f.read())
        self.assertEqual(type(data), dict)
        for key in data["0"].keys():
            self.assertTrue(key in self.life_headings)
        for age in sample_json_results:
            for key in sample_json_results[age]:
                self.assertEqual(sample_json_results[age][key], data[age][key])

    def test_make_soup(self):
        """Given a url, make a request and return beautifulsoup for parsing."""
        url = "http://www.socialsecurity.gov/OACT/ProgData/nra.html"
        soup = make_soup(url)
        self.assertTrue("Social Security" in soup.find("h1").text)

    @mock.patch("requests.get")
    def test_make_soup_error(self, mock_requests):
        url = "http://www.socialsecurity.gov/xxxx/"
        mock_requests.return_value.reason = "Not found"
        soup = make_soup(url)
        self.assertEqual(soup, "")

    # @mock.patch('utils.ss_update_stats.requests.get')
    # @mock.patch('utils.ss_update_stats.update_life')

    @mock.patch("retirement_api.utils.ss_update_stats.update_life")
    @mock.patch("retirement_api.utils.ss_update_stats.update_cola")
    @mock.patch("retirement_api.utils.ss_update_stats.update_awi_series")
    @mock.patch(
        "retirement_api.utils.ss_update_stats.update_example_reduction"
    )
    def test_harvest_all(
        self,
        mock_update_example,
        mock_update_awi,
        mock_update_cola,
        mock_update_life,
    ):
        utils.ss_update_stats.harvest_all()
        assert mock_update_example.call_count == 1
        assert mock_update_awi.call_count == 1
        assert mock_update_cola.call_count == 1
        assert mock_update_life.call_count == 1

    @mock.patch("retirement_api.utils.ss_update_stats.output_csv")
    @mock.patch("retirement_api.utils.ss_update_stats.output_json")
    @mock.patch("retirement_api.utils.ss_update_stats.make_soup")
    def test_example_reduction(
        self, mock_soup, mock_output_json, mock_output_csv
    ):
        # arrange
        with open(self.earlyretire_page, "r") as f:
            mockpage = f.read()
        mock_soup.return_value = bs(mockpage, "html.parser")

        # action
        utils.ss_update_stats.update_example_reduction()

        # assert

        assert mock_soup.call_count == 1
        assert mock_output_csv.call_count == 1
        assert mock_output_json.call_count == 1

    @mock.patch("retirement_api.utils.ss_update_stats.output_csv")
    @mock.patch("retirement_api.utils.ss_update_stats.output_json")
    @mock.patch("retirement_api.utils.ss_update_stats.make_soup")
    def test_update_life(self, mock_soup, mock_output_json, mock_output_csv):
        # arrange
        with open(self.life_page, "r") as f:
            mockpage = f.read()
        mock_soup.return_value = bs(mockpage, "html.parser")

        # action
        utils.ss_update_stats.update_life()

        # assert

        assert mock_soup.call_count == 1
        assert mock_output_csv.call_count == 1
        assert mock_output_json.call_count == 1

    @mock.patch("retirement_api.utils.ss_update_stats.output_csv")
    @mock.patch("retirement_api.utils.ss_update_stats.output_json")
    @mock.patch("retirement_api.utils.ss_update_stats.make_soup")
    def test_update_cola(self, mock_soup, mock_output_json, mock_output_csv):
        # arrange
        with open(self.cola_page, "r") as f:
            mockpage = f.read()
        mock_soup.return_value = bs(mockpage, "html.parser")

        # action
        utils.ss_update_stats.update_cola()

        # assert
        assert mock_soup.call_count == 1
        assert mock_output_csv.call_count == 1
        assert mock_output_json.call_count == 1

    @mock.patch("retirement_api.utils.ss_update_stats.output_csv")
    @mock.patch("retirement_api.utils.ss_update_stats.output_json")
    @mock.patch("retirement_api.utils.ss_update_stats.make_soup")
    def test_update_awi_series(
        self, mock_soup, mock_output_json, mock_output_csv
    ):
        # arrange
        with open(self.awi_page, "r") as f:
            mockpage = f.read()
        mock_soup.return_value = bs(mockpage, "html.parser")

        # action
        utils.ss_update_stats.update_awi_series()

        # assert
        assert mock_soup.call_count == 1
        assert mock_output_csv.call_count == 1
        assert mock_output_json.call_count == 1
