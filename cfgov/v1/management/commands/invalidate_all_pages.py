from django.conf import settings
from django.core.management.base import BaseCommand

from v1.models.akamai_backend import AkamaiBackend


class Command(BaseCommand):
    help = 'Invalidates entire cfgov site'

    def handle(self, *args, **options):
        AkamaiBackend(settings.WAGTAILFRONTENDCACHE['akamai']).purge_all()
