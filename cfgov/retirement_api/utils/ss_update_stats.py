import csv
import datetime
import json
import logging
import os
import sys

import requests
from bs4 import BeautifulSoup as bs


"""
terms:
    PIA:  Primary Insurance Amount, the basic SS benefit
    AIME: Average Indexed Monthly Earnings
"""

# from django.template.defaultfilters import slugify

TODAY = datetime.datetime.now().date()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
APP_DIR = "%s/retirement_api" % BASE_DIR

data_dir = "%s/data" % APP_DIR
backup_dir = "%s/data/backups" % APP_DIR
outcsv = "%s/early_penalty_%s.csv" % (data_dir, TODAY.year)
outjson = "%s/early_penalty_%s.json" % (data_dir, TODAY.year)

ss_table_urls = {
    "cola": "http://www.socialsecurity.gov/OACT/COLA/colaseries.html",
    "actuarial_life": "http://www.socialsecurity.gov/OACT/STATS/table4c6.html",
    # handled by get_retirement_age()
    "retirement_ages": "http://www.socialsecurity.gov/OACT/ProgData/nra.html",
    # not needed if we use SS calculator
    "benefit_bases": "http://www.socialsecurity.gov/OACT/COLA/cbb.html",
    "delay_credits": "http://www.socialsecurity.gov/retire2/delayret.htm",
    "awi_series": "http://www.socialsecurity.gov/OACT/COLA/AWI.html",
    # not needed if we use SS calculator
    "bend_points": "http://www.socialsecurity.gov/OACT/COLA/bendpoints.html",
    # useful as viz
    "early_retirement_example": "http://www.socialsecurity.gov/OACT/quickcalc/earlyretire.html",  # noqa: E501
    # info only
    "explainer of AMI calculations": "http://www.socialsecurity.gov/OACT/COLA/piaformula.html",  # noqa: E501
    # explanation of terms; info only
    "benefit_terms": "http://www.socialsecurity.gov/OACT/COLA/Benefits.html#aime",  # noqa: E501
    # out of scope: rules for achieving 40 work credits (10 years of work);
    # not envisioned for app
    "credit_rules": "http://www.socialsecurity.gov/planners/retire/credits2.html",  # noqa: E501
    # out of scope: basic work-credit unit to determine whether a worker is
    # covered by SS; you can earn 4 credits a year
    "quarter_of_coverage": "http://www.socialsecurity.gov/OACT/COLA/QC.html",
    # out of scope:
    # historical and projected male/female death probability tables
    "death_probabilities": "http://www.socialsecurity.gov/OACT/HistEst/DeathProbabilities2014.html",  # noqa: E501
    # out of scope: compendium of bend points,
    # COlA and other adjustment values used in SS calculations
    "automatic_values": "http://www.socialsecurity.gov/OACT/COLA/autoAdj.html",
}


log = logging.getLogger(__name__)


def output_csv(filepath, headings, bs_rows):
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerow(headings)
        for row in bs_rows:
            writer.writerow(
                [
                    cell.text.replace(",", "").strip()
                    for cell in row.findAll("td")
                    if row.findAll("td")
                ]
            )


def output_json(filepath, headings, bs_rows):
    json_out = {}
    for row in bs_rows:
        cells = [
            cell.text.replace(",", "").strip()
            for cell in row.findAll("td")
            if row.findAll("td")
        ]
        if len(cells) == 2:
            json_out[cells[0]] = cells[1]
        else:
            tups = zip(headings[1:], cells[1:])
            tupd = {}
            for tup in tups:
                tupd[tup[0]] = tup[1]
            json_out[cells[0]] = tupd
    with open(filepath, "w") as f:
        f.write(json.dumps(json_out))


def make_soup(url):
    req = requests.get(url)
    if req.reason != "OK":
        log.warn(
            "request to %s failed: %s %s" % (url, req.status_code, req.reason)
        )
        return ""
    else:
        soup = bs(req.text, "html.parser")
        return soup


def update_example_reduction():
    """
    SSA's example shows Primary and spousal benefits at age 62,
    assuming a primary insurance amount of $1,000
    """
    url = ss_table_urls["early_retirement_example"]
    headings = [
        "YOB",
        "FRA",
        "reduction_months",
        "primary_pia",
        "primary_pct_reduction",
        "spouse_pia",
        "spouse_pct_reduction",
    ]
    soup = make_soup(url)
    if soup:
        table = soup.findAll("table")[5].find("table")
        rows = [row for row in table.findAll("tr") if row.findAll("td")]
        output_csv(outcsv, headings, rows)
        log.info("updated %s with %s rows" % (outcsv, len(rows)))
        output_json(outjson, headings, rows)
        log.info("updated %s with %s entries" % (outjson, len(rows)))


def update_awi_series():
    url = ss_table_urls["awi_series"]
    outcsv = "%s/awi_series_%s.csv" % (data_dir, TODAY.year)
    outjson = "%s/awi_series_%s.json" % (data_dir, TODAY.year)
    headings = ["Year", "Index"]
    soup = make_soup(url)
    if soup:
        tables = soup.findAll("table")[1].findAll("table")
        rows = []
        log.info("found %s tables" % len(tables))
        for table in tables:
            rows.extend(
                [row for row in table.findAll("tr") if row.findAll("td")]
            )
        output_csv(outcsv, headings, rows)
        log.info("updated %s with %s rows" % (outcsv, len(rows)))
        output_json(outjson, headings, rows)
        log.info("updated %s with %s entries" % (outjson, len(rows)))


def update_cola():
    url = ss_table_urls["cola"]
    outcsv = "%s/ss_cola_%s.csv" % (data_dir, TODAY.year)
    outjson = "%s/ss_cola_%s.json" % (data_dir, TODAY.year)
    headings = ["Year", "COLA"]
    soup = make_soup(url)
    if soup:
        [s.extract() for s in soup("small")]
        tables = soup.findAll("table")[-3:]
    rows = []
    log.info("found %s tables" % len(tables))
    for table in tables:
        rows.extend([row for row in table.findAll("tr") if row.findAll("td")])
    output_csv(outcsv, headings, rows)
    log.info("updated %s with %s rows" % (outcsv, len(rows)))
    output_json(outjson, headings, rows)
    log.info("updated %s with %s entries" % (outjson, len(rows)))


def update_life():
    """update the actuarial life tables from SSA"""
    msg = ""
    url = ss_table_urls["actuarial_life"]
    # outcsv = "%s/actuarial_life_%s.csv" % (data_dir, TODAY.year)
    # outjson = "%s/actuarial_life_%s.json" % (data_dir, TODAY.year)
    headings = [
        "exact_age",
        "male_death_probability",
        "male_number_of_lives",
        "male_life_expectancy",
        "female_death_probability",
        "female_number_of_lives",
        "female_life_expectancy",
    ]
    soup = make_soup(url)
    if soup:
        table = soup.find("table").find("table")
        if not table:
            log.info("couldn't find table at %s" % url)
        else:
            rows = table.findAll("tr")[2:]
            if len(rows) > 100:
                output_csv(outcsv, headings, rows)
                msg += "updated %s with %s rows" % (outcsv, len(rows))
                output_json(outjson, headings, rows)
                msg += "updated {0} with {1} entries".format(
                    outjson, len(rows)
                )
            else:
                msg += "didn't find more than 100 rows at {0}".format(url)
    log.info(msg)
    return msg


def harvest_all():
    update_life()
    update_cola()
    update_awi_series()
    update_example_reduction()


if __name__ == "__main__":
    starter = datetime.datetime.now()
    harvest_all()
    log.info(
        "update took {0} to update four data stores".format(
            (datetime.datetime.now() - starter)
        )
    )
