from django.conf import settings
from django.core.management.base import BaseCommand

from v1.models.caching import AkamaiBackend


class Command(BaseCommand):
    help = "Delete entire cfgov site cache"

    def handle(self, *args, **options):
        AkamaiBackend(settings.WAGTAILFRONTENDCACHE["akamai"]).delete_all()
