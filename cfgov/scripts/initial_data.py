import os, json

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from wagtail.wagtailcore.models import Page, Site

from v1.models import HomePage, BrowseFilterablePage


def run():
    if settings.DEBUG:
        print 'Running script \'scripts.initial_data\' ...'
        admin_user = None
        site_root = None
        events = None

        admin_user = User.objects.filter(username='admin')
        if not admin_user:
            admin_user = User(username='admin',
                              password=make_password(os.environ.get('WAGTAIL_ADMIN_PW')),
                              is_superuser=True, is_active=True, is_staff=True)
            admin_user.save()
        else:
            admin_user = admin_user[0]

        # Creates a new site root `CFGov`
        site_root = HomePage.objects.filter(title='CFGOV')
        if not site_root:
            root = Page.objects.first()
            site_root = HomePage(title='CFGOV', slug='home', depth=2, owner=admin_user)
            site_root.live = True
            root.add_child(instance=site_root)
            latest = site_root.save_revision(user=admin_user, submitted_for_moderation=False)
            latest.save()
        else:
            site_root = site_root[0]

        # Setting new site root
        if not Site.objects.filter(hostname='content.localhost').exists():
            site = Site.objects.first()
            site.port = 8000
            site.root_page_id = site_root.id
            site.save()
            content_site = Site(hostname='content.localhost', port=8000, root_page_id=site_root.id)
            content_site.save()

            # Clean Up
            old_site_root = Page.objects.filter(id=2)[0]
            if old_site_root:
                old_site_root.delete()

        # Events Browse Page required for event `import-data` command
        if not BrowseFilterablePage.objects.filter(title='Events').exists():
            events = BrowseFilterablePage(title='Events', slug='events', owner=admin_user)
            site_root.add_child(instance=events)
            revision = events.save_revision(
                user=admin_user,
                submitted_for_moderation=False,
            )
            revision.publish()

        # Archived Events Browse Filterable Page
        if not BrowseFilterablePage.objects.filter(title='Archive').exists():
            archived_events = BrowseFilterablePage(title='Archive', slug='archive', owner=admin_user)
            if not events:
                events = BrowseFilterablePage.objects.get(title='Events')

            events.add_child(instance=archived_events)
            revision = archived_events.save_revision(
                user=admin_user,
                submitted_for_moderation=False,
            )
            revision.publish()
