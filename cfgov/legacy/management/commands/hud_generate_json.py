from __future__ import absolute_import, unicode_literals

import logging

from django.core.management.base import BaseCommand, CommandError

from legacy.housing_counselor.cleaner import clean_counselors
from legacy.housing_counselor.fetcher import fetch_counselors
from legacy.housing_counselor.generator import generate_counselor_json
from legacy.housing_counselor.geocoder import (
    GazetteerZipCodeFile, GeocodedZipCodeCsv, geocode_counselors
)


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate bulk housing counselor JSON data'

    def add_arguments(self, parser):
        parser.add_argument('target', help='JSON output directory')
        parser.add_argument('--zipcode-csv-file',
                            help='CSV containing zipcode lat/lngs')
        parser.add_argument('--zipcode-gazetteer-file',
                            help='Census Gazetteer zipcode file')

    def handle(self, *args, **options):
        zipcode_csv_file = options['zipcode_csv_file']
        zipcode_gazetteer_file = options['zipcode_gazetteer_file']

        if zipcode_csv_file:
            zipcodes = GeocodedZipCodeCsv.read(zipcode_csv_file)
        elif zipcode_gazetteer_file:
            zipcodes = GazetteerZipCodeFile.read(zipcode_gazetteer_file)
        else:
            raise CommandError(
                'One of --zipcode-csv-file or --zipcode-gazetteer-file '
                'must be provided to enable mapping from zipcode to '
                'latitude/longitude coordinates.'
            )

        # Retrieve counselors from the HUD website.
        counselors = fetch_counselors()

        # Standardize formatting of counselor data.
        counselors = clean_counselors(counselors)

        # Add in any missing latitude/longitude information for counselors.
        counselors = geocode_counselors(counselors, zipcodes=zipcodes)

        # Generate JSON files for each zipcode.
        generate_counselor_json(counselors, zipcodes, options['target'])
