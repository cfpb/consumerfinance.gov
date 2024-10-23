from django.conf import settings
from django.core.management.base import BaseCommand

from cdntools.backends import AkamaiBackend


class Command(BaseCommand):
    help = "Invalidate entire cfgov site cache"

    def handle(self, *args, **options):
        AkamaiBackend(settings.WAGTAILFRONTENDCACHE["akamai"]).purge_all()
