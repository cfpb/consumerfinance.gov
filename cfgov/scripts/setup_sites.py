from wagtail.wagtailcore.models import Site
from django.conf import settings


def run(hostname):
    if settings.DEBUG:
        # Set up sites
        live = 'localhost'
        shared = 'content.' + live
        port = 8000
        if hostname:
            live = str(hostname)
            shared = 'content.' + live
            port = 80

        site1 = Site.objects.first()
        site1.hostname = live
        site1.port = port
        site1.save()
        site2 = Site.objects.last()
        site2.hostname = shared
        site2.port = port
        site2.save()
