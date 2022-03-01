import glob
import json
import logging
import os
import re
import sqlite3
from math import acos, cos, radians, sin

from django.template import loader


logger = logging.getLogger(__name__)


def distance_in_miles(lat1_radians, lng1_radians, lat2_radians, lng2_radians):
    """Estimate distance in miles between two points in radians.

    Uses simplified algorithm to determine proximity based on latitude and
    longitude, described at https://stackoverflow.com/q/1916953.
    """
    if lat1_radians == lat2_radians and lng1_radians == lng2_radians:
        return 0

    earth_radius_in_miles = 3959

    return earth_radius_in_miles * acos(
        cos(lat1_radians)
        * cos(lat2_radians)
        * cos(lng2_radians - lng1_radians)
        + sin(lat1_radians) * sin(lat2_radians)
    )


def get_db_connection():
    connection = sqlite3.connect(":memory:")
    connection.create_function("distance_in_miles", 4, distance_in_miles)

    return connection


def fill_db(connection, counselors):
    def prepare_counselors(counselors):
        for counselor in counselors:
            yield (
                radians(float(counselor["agc_ADDR_LATITUDE"])),
                radians(float(counselor["agc_ADDR_LONGITUDE"])),
                json.dumps(counselor),
            )

    create_sql = """
CREATE TABLE counselors (
    latitude_radians REAL,
    longitude_radians REAL,
    json TEXT
)
"""

    insert_sql = """
INSERT INTO
    counselors(latitude_radians, longitude_radians, json)
VALUES (?, ?, ?)
"""

    connection.execute(create_sql)
    connection.executemany(insert_sql, prepare_counselors(counselors))


def query_db(connection, latitude_radians, longitude_radians):
    sql = """
SELECT
    json,
    distance_in_miles(latitude_radians, longitude_radians, ?, ?) AS distance
FROM
    counselors
ORDER BY distance ASC
LIMIT 10
    """

    response = connection.execute(sql, (latitude_radians, longitude_radians))

    results = []
    for row in response:
        result = json.loads(row[0])
        result["distance"] = row[1]
        results.append(result)

    return results


def generate_counselor_json(counselors, zipcodes, target):
    connection = get_db_connection()
    fill_db(connection, counselors)

    logger.info("generating JSON into %s", target)

    for zipcode, (latitude_degrees, longitude_degrees) in zipcodes.items():
        counselors = query_db(
            connection, radians(latitude_degrees), radians(longitude_degrees)
        )

        zipcode_data = {
            "zip": {
                "zipcode": zipcode,
                "lat": latitude_degrees,
                "lng": longitude_degrees,
            },
            "counseling_agencies": counselors,
        }

        json_filename = os.path.join(target, "{}.json".format(zipcode))

        with open(json_filename, "w") as f:
            f.write(json.dumps(zipcode_data))


def generate_counselor_html(source_dir, target_dir):
    template_name = "housing_counselor/pdf_selfcontained.html"
    template = loader.get_template(template_name)

    for zipcode, filename in get_counselor_json_files(source_dir):
        with open(filename, "r") as f:
            zipcode_data = json.loads(f.read())

        html = template.render(
            {
                "zipcode": zipcode,
                "zipcode_valid": True,
                "api_json": zipcode_data,
            }
        )

        html_filename = os.path.join(target_dir, "{}.html".format(zipcode))

        with open(html_filename, "w") as f:
            f.write(html)


def get_counselor_json_files(directory):
    """Returns an iterable list of JSON files and associated zipcodes.

    Returns iterator of (zipcode, filename) pairs.
    """
    search_path = os.path.join(directory, "*.json")
    filenames = list(
        filter(lambda f: re.search(r"/\d{5}.json$", f), glob.glob(search_path))
    )

    if not filenames:
        raise RuntimeError("no input files found in {}".format(directory))

    logger.info("Found %d input files", len(filenames))

    for filename in filenames:
        match = re.search(r"/(\d{5}).json$", filename)
        zipcode = match.group(1)

        yield zipcode, filename
