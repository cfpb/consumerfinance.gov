from django.core.management.base import BaseCommand

from data_research.research_conference import ConferenceExporter


class Command(BaseCommand):
    help = "Exports research conference registrants as Excel workbook"

    def add_arguments(self, parser):
        parser.add_argument(
            "govdelivery_code",
            help=("Export conference registrations for this GovDelivery code"),
        )
        parser.add_argument(
            "xlsx_filename", help="Save Excel workbook to this local filename"
        )

    def handle(self, *args, **options):
        exporter = ConferenceExporter(options["govdelivery_code"])
        exporter.save_xlsx(options["xlsx_filename"])
