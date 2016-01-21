import os

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from v1.models.events import EventLandingPage
from wagtail.wagtailcore.models import Page


def run():
    if settings.DEBUG:
        print 'Running script \'scripts.initial_data\' ...'

        if not User.objects.filter(username='admin').exists():
            admin_user = User(username='admin',
                              password=make_password(os.environ.get('WAGTAIL_ADMIN_PW')),
                              is_superuser=True, is_active=True, is_staff=True)
            admin_user.save()
        # Renaming Site root name to `V1`
        if not Page.objects.filter(title='V1').exists():
            site_root = Page.objects.get(id=2)
            site_root.title = 'V1'
            site_root.save()
        # Events Landing Page required for event `import-data` command
        if not EventLandingPage.objects.filter(title='Events').exists():
            events = EventLandingPage(title='Events', slug='events')
            site_root.add_child(instance=events)
            revision = events.save_revision(
                submitted_for_moderation=False,
            )
            revision.publish()
