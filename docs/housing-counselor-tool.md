# Find a Housing Counselor

The [Find a Housing Counselor tool](https://www.consumerfinance.gov/find-a-housing-counselor/) allows users to search for HUD-approved housing counselors.
Users enter a U.S. ZIP code, and the tool returns a list of the ten housing counselors nearest to that ZIP code location.
The page also displays a map of the results using Mapbox.

When the user enters a ZIP code in the page's search box, the [Django view](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/views.py#L84) fetches a JSON file of the results from our Amazon S3 bucket.
The results are inserted into the [page template](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/jinja2/housing_counselor/index.html) and the [Mapbox map](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/unprocessed/apps/find-a-housing-counselor/js/common.js).
The page also contains a link to a PDF version of the results, which is also stored in S3.
The files are publicly accessible, so the tool can run on localhost or in a container without any change in behavior.

This page documents the process we use to generate the JSON and PDF files the Find a Housing Counselor tool relies on.


## Housing Counselor Data Processing

The tool gets its data from the U.S. Department of Housing and Urban Development (HUD).
HUD provides an [API](https://data.hud.gov/housing_counseling.html) to their list of approved counseling agencies.
A daily job, `cf.gov-housing-counselor-data` on our external Jenkins server,
queries HUD data and produces the JSON and PDF files we use for the Find a Housing Counselor tool.
It performs the following steps, each of which is optional
and configured using parameters before starting the job.

  1. [Geocode ZIP codes](#geocode-zip-codes) (`GEOCODE_ZIPCODES`)
  2. [Generate JSON files](#generate-json-files) (`MAKE_JSON`)
  3. [Generate HTML files](#generate-html-files) (`MAKE_HTML`)
  4. [Generate PDFs](#generate-pdfs) (`MAKE_PDF`)
  5. [Upload to S3](#upload-to-s3) (`UPLOAD_TO_S3`)


### Geocode ZIP codes

The `GEOCODE_ZIPCODES` step generates a file of all ZIP codes in the United States and their location latitude and longitude and saves it in the Jenkins workspace.
By default, this step is not enabled.
Since ZIP code geographical information rarely changes, we run this step rarely by manually enabling the option in the Jenkins job.

If enabled, this step calls the [`hud_geocode_zipcodes`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/management/commands/hud_geocode_zipcodes.py) management command.
The management command in turn calls the `BulkZipCodeGeocoder` in [`geocoder.py`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/geocoder.py).
`BulkZipCodeGeocoder` uses the [Mapbox](https://www.mapbox.com/) geocoding API to determine which 5-digit number sequences are ZIP codes and fetch their latitude and longitude values.
The management command inserts this data into a CSV and saves it to `./zipcodes.csv` on the Jenkins job workspace.

The generated file looks like this:

```csv
12305,42.81,-73.94
12306,42.77,-73.96
12307,42.81,-73.93
12308,42.82,-73.93
12309,42.81,-73.91
12325,42.88779,-73.99597
12345,42.80856,-74.02737
```


### Generate JSON files

When enabled, the `MAKE_JSON` step generates a JSON file of housing counselor data for each ZIP code in the U.S.
Each file contains the ten results geographically nearest to the ZIP code's latitude and longitude.
This step is enabled by default.

This step calls the [`hud_generate_json`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/management/commands/hud_generate_json.py) management command,
which performs the following steps:

  1. fetch agency listings from HUD
  2. save a copy of the full results, for our records
  3. clean the results
  4. fill in any missing latitude and longitude values
  5. create files of the 10 nearest results for each U.S. ZIP code


#### Fetch agency listings

(_in [`fetcher.py`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/fetcher.py)_)

Request every housing counselor in HUD's database
with a request to `https://data.hud.gov/Housing_Counselor/searchByLocation?Lat=38.8951&Long=-77.0367&Distance=5000`.

It returns thousands of results like this:

```json
{
    "services": "DFC,FBC,PPC,RHC",
    "languages": "ENG,SPA",
    "agc_STATUS": "A",
    "agc_SRC_CD": "HUD",
    "counslg_METHOD": "Face to Face Counseling,Group Counseling,Phone Counseling",
    "agcid": "80790",
    "adr1": "1234 N. Example St.",
    "adr2": " ",
    "city": "SPRINGFIELD",
    "email": "counselor@example.org",
    "fax": "999-888-7777",
    "nme": "EXAMPLE COMMUNITY HOUSING SERVICES",
    "phone1": "111-222-3333",
    "statecd": "MI",
    "weburl": "www.example.org",
    "zipcd": "48219-8888",
    "agc_ADDR_LATITUDE": "42.442658",
    "agc_ADDR_LONGITUDE": "-83.28329",
    "parentid": "81228",
    "county_NME": "",
    "phone2": " ",
    "mailingadr1": "1234 N. Example St.",
    "mailingadr2": " ",
    "mailingcity": "SPRINGFIELD",
    "mailingzipcd": "48219-8888",
    "mailingstatecd": "MI",
    "state_NME": "Michigan",
    "state_FIPS_CODE": null,
    "faithbased": "N",
    "colonias_IND": "Y",
    "migrantwkrs_IND": "N"
},
```

Next, we replace the `languages` value with the full language names.
We replace the `services` value with fully spelled out service descriptions.
Both of these mappings come from the HUD API.

#### Save the results

(_in [`results_archiver.py`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/results_archiver.py)_)

Save a copy of the full set of results as a zip file in the home directory.
The Jenkins job then transfers the zip file to S3 as part of the `MAKE JSON` step.
The file is saved in S3 at `/archive/{date}.zip`.
This copy can be used as the canonical set of HUD data that day in case of an enforcement action.

#### Clean the results

(_in [`cleaner.py`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/cleaner.py)_)

Clean the data: Convert latitude and longitude values to float values.
Convert the the city and organization name to title case.
Ensure email appears to be an email (otherwise leave it blank).
If a URL value is present, ensure it begins with `http://`.

#### Backfill missing latitude and longitude values

(_in [`geocoder.py`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/geocoder.py)_)

If any counselor records are missing their latitude or longitude data,
we fill in those values with the lat/long location of the agency's ZIP code.
This uses the data file created in the Geocode ZIP Codes stage of the Jenkins job ([above](#geocode-zip-codes)).

#### Create collections of results by ZIP code

(_in [`generator.py`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/generator.py)_)

Create an in-memory SQLite database and define a `distance_in_miles` function in it.
Fill the database with a three-column table:
For each counselor in the list, include its latitude and longitude (both in radians) and
all of its information from the HUD API as a JSON text string.

For each ZIP code in the U.S., query the database to find the 10 closest housing counselors to the lat/long of that ZIP.
Put the information in a JSON structure like this (but with ten results instead of one):

```json
{
    "zip": {
        "lat": 42.80856,
        "lng": -74.02737,
        "zipcode": "12345"
    },
    "counseling_agencies": [{
        "adr1": "1234 N. Example St.",
        "state_FIPS_CODE": null,
        "adr2": " ",
        "zipcd": "48219-8888",
        "mailingcity": "Springfield",
        "weburl": "http://www.example.org",
        "agc_STATUS": "A",
        "city": "Springfield",
        "languages": ["English", "Spanish"],
        "faithbased": "N",
        "mailingstatecd": "MI",
        "email": "counselor@example.org",
        "fax": "999-888-7777",
        "phone1": "111-222-3333",
        "distance": 5.430720023569205,
        "phone2": " ",
        "agc_ADDR_LATITUDE": 42.442658,
        "agcid": "80790",
        "agc_SRC_CD": "HUD",
        "nme": "Example Community Housing Services",
        "migrantwkrs_IND": "N",
        "parentid": "82772",
        "services": ["Mortgage Delinquency and Default Resolution Counse", "Home Improvement and Rehabilitation Counseling", "Pre-purchase Counseling", "Pre-purchase Homebuyer Education Workshops", "Rental Housing Counseling"],
        "counslg_METHOD": "Face to Face Counseling,Group Counseling,Phone Counseling",
        "county_NME": "",
        "mailingadr1": "1234 N. Example St.",
        "statecd": "MI",
        "mailingadr2": " ",
        "mailingzipcd": "48219-8888",
        "state_NME": "Michigan",
        "agc_ADDR_LONGITUDE": -83.28329,
        "colonias_IND": "Y"
    }]
}
```

Save the resulting JSON files on the Jenkins job workspace, in a `jsons` directory, e.g. `jsons/12345.json`.


### Generate HTML files

When enabled, the `MAKE_HTML` step generates an HTML page of housing counselor results, including styles,
for each file created in the previous step.
It saves them in an `htmls` directory on the Jenkins job workspace.
This step is enabled by default.

This step calls the [`hud_generate_html`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/management/commands/hud_generate_html.py) management command,
which calls HTML generation code in [`generator.py`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/generator.py).
Django renders the [`housing_counselor/pdf_selfcontained.html`](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/housing_counselor/templates/housing_counselor/pdf_selfcontained.html) template with the housing counselor data from each JSON file.
We save the resulting HTML files on the Jenkins job workspace, in a `htmls` directory, e.g. `htmls/12345.html`.


### Generate PDFs

When enabled, the `MAKE_PDF` step generates a PDF of each file created in the previous step.
It saves them in a `pdfs` directory on the Jenkins job workspace.
This step is enabled by default.

This step uses a HTML to PDF conversion command line tool.
We run the conversion on each file in the `htmls` directory, generating a PDF version of each, e.g. `pdfs/12345.pdf`.


### Upload to S3

When enabled, the `UPLOAD_TO_S3` step uploads the contents of the `jsons` and `pdfs` directories to an Amazon S3 bucket where it can be accessed by consumerfinance.gov.
This step is enabled by default.

The files are publicly accessible, e.g.:

 - https://files.consumerfinance.gov/a/assets/hud/jsons/12345.json
 - https://files.consumerfinance.gov/a/assets/hud/pdfs/12345.pdf
