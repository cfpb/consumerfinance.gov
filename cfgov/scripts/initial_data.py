import os

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from v1.models.browse_page import BrowsePage
from v1.models.browse_filterable_page import BrowseFilterablePage
from wagtail.wagtailcore.models import Page


def run():
    if settings.DEBUG:
        print 'Running script \'scripts.initial_data\' ...'
        admin_user = None
        site_root = None
        events = None

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
        # Events Browse Page required for event `import-data` command
        if not BrowsePage.objects.filter(title='Events').exists():
            if not admin_user:
                admin_user = User.objects.filter(username='admin')[0]

            events = BrowsePage(title='Events', slug='events', owner=admin_user)
            if not site_root:
                site_root = Page.objects.get(title='V1')

            site_root.add_child(instance=events)
            revision = events.save_revision(
                user=admin_user,
                submitted_for_moderation=False,
            )
            revision.publish()
        # Archived Events Browse Filterable Page
        if not BrowseFilterablePage.objects.filter(title='Archive').exists():
            if not admin_user:
                admin_user = User.objects.filter(username='admin')[0]

            archived_events = BrowseFilterablePage(title='Archive', slug='archive', owner=admin_user)
            if not events:
                events = BrowsePage.objects.get(title='Events')

            events.add_child(instance=archived_events)
            revision = archived_events.save_revision(
                user=admin_user,
                submitted_for_moderation=False,
            )
            revision.publish()
