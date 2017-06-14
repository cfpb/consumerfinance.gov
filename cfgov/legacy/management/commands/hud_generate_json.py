from __future__ import absolute_import, unicode_literals

import csv

from django.core.management.base import BaseCommand
from six import print_

from legacy.housing_counselor.cleaner import clean_counselors
from legacy.housing_counselor.fetcher import fetch_counselors
from legacy.housing_counselor.generator import generate_counselor_json


def load_zipcodes(filename):
    """Load zipcode location data from Census gazetteer file.

    See https://www.census.gov/geo/maps-data/data/gazetteer2016.html

    Returns a tuple: (zipcode, latitude_degreees, longitude_degrees)
    """
    print_('Reading zipcodes from', filename, flush=True)
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=str('\t'))
        next(reader)

        zipcodes = dict(
            (row[0], (float(row[5].strip()), float(row[6].strip())))
            for row in reader
        )

    print_('Loaded', len(zipcodes), 'zipcodes', flush=True)
    return zipcodes


class Command(BaseCommand):
    help = 'Generate bulk housing counselor JSON data'

    def add_arguments(self, parser):
        parser.add_argument('zipcode_filename')
        parser.add_argument('target')

    def handle(self, *args, **options):
        zipcodes = load_zipcodes(options['zipcode_filename'])

        # Retrieve counselors from the HUD website.
        counselors = fetch_counselors()

        # Add in any missing latitude/longitude information for counselors.
        # This is not required due to the way that counselors are fetched
        # by location, but can be reenabled should fetching change in future.
        # counselors = geocode_counselors(counselors, zipcodes=zipcodes)

        # Standardize formatting of counselor data.
        counselors = clean_counselors(counselors)

        # Generate JSON files for each zipcode.
        generate_counselor_json(counselors, zipcodes, options['target'])
