import json
from csv import DictReader as cdr


"""
# Data processing steps

This script was used to process a few xlsx files to look at expediture data
based on income and region
- source: http://www.bls.gov/cex/
- files under Region of residence by income before taxes:
  - xregnmw.xlsx
  - xregnne.xlsx
  - xregns.xlsx
  - xregnw.xlsx

The xlsx were converted manually using the following steps:
- convert xlsx to csv
- delete the top 1 line, which are fake headings
- remove newline characters on the first line (the real headings)
- Remove everything from the line "Addenda:" to the end

To run from the script from the Django shell, if xlsx files are not
in the default location provided, you can also specify them as
arguments:

```
./manage.py shell
from paying_for_college.data_sources.bls_processing import *
create_bls_json_file()
```

This will create a new file in `paying_for_college/fixtures/bls_data.json`

"""

BASE_DIR = "paying_for_college/data_sources"
WE_CSVFILE = "{}/xregnw.csv".format(BASE_DIR)
NE_CSVFILE = "{}/xregnne.csv".format(BASE_DIR)
MW_CSVFILE = "{}/xregnmw.csv".format(BASE_DIR)
SO_CSVFILE = "{}/xregns.csv".format(BASE_DIR)
YEAR = 2014

OUT_FILE = "paying_for_college/fixtures/bls_data.json"


def load_bls_data(csvfile):

    with open(csvfile, "rU") as f:
        reader = cdr(f)
        return [row for row in reader]


def add_bls_dict_with_region(base_bls_dict, region, csvfile):

    CATEGORIES_KEY_MAP = {
        "Food": "Food",
        "Housing": "Housing",
        "Transportation": "Transportation",
        "Healthcare": "Healthcare",
        "Entertainment": "Entertainment",
        "Personal insurance and pensions": "Retirement",
        "Apparel and services": "Clothing",
        "Personal taxes (contains some imputed values)": "Taxes",
        # Other
        "Alcoholic beverages": "Other",
        "Personal care products and services": "Other",
        "Reading": "Other",
        "Education": "Other",
        "Tobacco products and smoking supplies": "Other",
        "Miscellaneous": "Other",
        "Cash contributions": "Other",
    }

    INCOME_KEY_MAP = {
        "Less than $5,000": "less_than_5000",
        "$5,000 to $9,999": "5000_to_9999",
        "$10,000 to $14,999": "10000_to_14999",
        "$15,000 to $19,999": "15000_to_19999",
        "$20,000 to $29,999": "20000_to_29999",
        "$30,000 to $39,999": "30000_to_39999",
        "$40,000 to $49,999": "40000_to_49999",
        "$50,000 to $69,999": "50000_to_69999",
        "$70,000 and more": "70000_or_more",
    }

    data = load_bls_data(csvfile)
    print("******Processing {} file...******".format(region))
    for row in data:
        item = row["Item"].strip()
        if item in CATEGORIES_KEY_MAP.keys():
            print("Current processing {}.....".format(item))
            print(
                "Will be adding {} to base_bls_dict...".format(
                    CATEGORIES_KEY_MAP[item]
                )
            )
            base_bls_dict[CATEGORIES_KEY_MAP[item]].setdefault(region, {})
            for income_key, income_json_key in INCOME_KEY_MAP.items():
                print("adding {} ...".format(income_key))
                amount = int(row[income_key].replace(",", ""))
                print("amount: {}".format(amount))
                base_bls_dict[CATEGORIES_KEY_MAP[item]][region].setdefault(
                    income_json_key, 0
                )
                base_bls_dict[CATEGORIES_KEY_MAP[item]][region][
                    income_json_key
                ] += amount  # noqa


def bls_as_dict(we_csvfile, ne_csvfile, mw_csvfile, so_csvfile):

    bls_dict = {
        "Food": {"note": "Dining out and in; all food costs"},
        "Housing": {"note": "Mortgage, rent, utilities, insurance"},
        "Transportation": {"note": "Cars, public transit, insurance"},
        "Healthcare": {"note": "Including insurance"},
        "Entertainment": {"note": "Events, pets, hobbies, equipment"},
        "Retirement": {"note": "Pensions and personal insurance"},
        "Clothing": {"note": "Apparel and services"},
        "Taxes": {
            "note": (
                "Personal federal, state, and local taxes; "
                "contains some imputed values"
            )
        },
        "Other": {"note": "Other expeditures"},
    }

    add_bls_dict_with_region(bls_dict, "WE", WE_CSVFILE)
    add_bls_dict_with_region(bls_dict, "NE", NE_CSVFILE)
    add_bls_dict_with_region(bls_dict, "MW", MW_CSVFILE)
    add_bls_dict_with_region(bls_dict, "SO", SO_CSVFILE)

    bls_dict["Year"] = YEAR

    return bls_dict


def create_bls_json_file(
    we_csvfile=WE_CSVFILE,
    ne_csvfile=NE_CSVFILE,
    mw_csvfile=MW_CSVFILE,
    so_csvfile=SO_CSVFILE,
):

    with open(OUT_FILE, "w") as outfile:
        bls_dict = bls_as_dict(we_csvfile, ne_csvfile, mw_csvfile, so_csvfile)
        json.dump(bls_dict, outfile)
