from django.core.management.base import BaseCommand

from data_research.models import ConferenceRegistration


class Command(BaseCommand):
    help = "Deletes research conference registrations"

    def add_arguments(self, parser):
        parser.add_argument(
            "govdelivery_code",
            help=("Delete conference registrations for this GovDelivery code"),
        )

    def handle(self, *args, **options):
        registrants = ConferenceRegistration.objects.filter(
            govdelivery_code=options["govdelivery_code"]
        )

        if options["verbosity"]:
            self.stdout.write("deleting %d registrants" % registrants.count())

        registrants.delete()
