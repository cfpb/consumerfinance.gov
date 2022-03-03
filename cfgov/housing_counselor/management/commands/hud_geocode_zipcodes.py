import logging

from django.core.management.base import BaseCommand

from housing_counselor.geocoder import BulkZipCodeGeocoder, GeocodedZipCodeCsv

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Geocode all possible zipcodes"

    def add_arguments(self, parser):
        parser.add_argument("output_filename", help="output CSV filename")
        parser.add_argument(
            "-c",
            "--continue-file",
            action="store_true",
            help="continue partially complete output file",
        )

    def handle(self, *args, **options):
        output_filename = options["output_filename"]
        logger.info("geocoding zipcodes to %s", output_filename)

        if options["continue_file"]:
            mode = "a"
            zipcodes = GeocodedZipCodeCsv.read(output_filename)
            start = int(max(zipcodes.keys())) + 1
        else:
            mode = "w"
            start = 0

        logger.info("starting geocoding at %s", start)
        zipcodes = BulkZipCodeGeocoder().geocode_zipcodes(start=start)

        with open(output_filename, mode) as f:
            GeocodedZipCodeCsv.write(f, zipcodes)
