from wagtail.wagtailcore.models import Site
from django.conf import settings


def run():
    if settings.DEBUG:
        # Set up sites
        site1 = Site.objects.first()
        site1.hostname = 'localhost'
        site1.port = 8000
        site1.save()
        site2 = Site.objects.last()
        site2.hostname = 'content.localhost'
        site2.port = 8000
        site2.save()
