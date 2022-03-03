import logging

from django.core.management.base import BaseCommand

from wagtail.core.models import Site

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sets default site hostname to provided argument"

    def add_arguments(self, parser):
        parser.add_argument(
            "--hostname",
            required=True,
            help='Hostname for default site, e.g. "beta.consumerfinance.gov"',
        )

    def handle(self, *args, **options):
        default_site = Site.objects.get(is_default_site=True)
        default_site.hostname = options["hostname"]
        default_site.save()
