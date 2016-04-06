import os, json

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from wagtail.wagtailcore.models import Page, Site

from v1.models import HomePage, BrowseFilterablePage, BrowsePage, DemoPage, SublandingPage, SublandingFilterablePage, \
    EventPage, DocumentDetailPage, EventArchivePage, LearnPage, LandingPage


def run():
    print 'Running script \'scripts.initial_test_data\' ...'

    admin_user = User.objects.filter(username='admin')
    if not admin_user:
        admin_user = User(username='admin',
                          password=make_password(os.environ.get('WAGTAIL_ADMIN_PW')),
                          is_superuser=True, is_active=True, is_staff=True)
        admin_user.save()
    else:
        admin_user = admin_user[0]


    # # Creates a new site root `CFGov`
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

    #Setting new site root
    site = Site.objects.first()
    if site.root_page_id != site_root.id:
        site.port = 8000
        site.root_page_id = site_root.id
        site.save()
        content_site = Site(hostname='content.localhost', port=8000, root_page_id=site_root.id)
        content_site.save()

    def publish_page(child=None, root=site_root):
        root.add_child(instance=child)
        revision = child.save_revision(
            user=admin_user,
            submitted_for_moderation=False,
        )
        revision.publish()

    # Create each Page Type
    if not LandingPage.objects.filter(title='Landing Page'):
        lap = LandingPage(title='Landing Page', slug='landing-page', owner=admin_user)
        publish_page(lap)

    if not SublandingPage.objects.filter(title='Sublanding Page'):
        sp = SublandingPage(title='Sublanding Page', slug='sublanding-page', owner=admin_user)
        publish_page(sp)

    if not BrowsePage.objects.filter(title='Browse Page'):
        bp = BrowsePage(title='Browse Page', slug='browse-page', owner=admin_user)
        publish_page(bp)

    # Filterable Pages
    if not BrowseFilterablePage.objects.filter(title='Browse Filterable Page'):
        bfp = BrowseFilterablePage(title='Browse Filterable Page', slug='browse-filterable-page', owner=admin_user)
        publish_page(bfp)

    if not SublandingFilterablePage.objects.filter(title='Sublanding Filterable Page'):
        sfp = SublandingFilterablePage(title='Sublanding Filterable Page', slug='sublanding-filterable-page',
                                       owner=admin_user)
        publish_page(sfp)

    if not EventArchivePage.objects.filter(title='Event Archive Page'):
        eap = EventArchivePage(title='Event Archive Page', slug='event-archive-page', owner=admin_user)
        publish_page(eap)

    # Filter Pages
    if not EventPage.objects.filter(title='Event Page'):
        ep = EventPage(title='Event Page', slug='event-page', owner=admin_user)
        publish_page(ep, bfp)

    if not DocumentDetailPage.objects.filter(title='Document Detail Page'):
        ddp = DocumentDetailPage(title='Document Detail Page', slug='document-detail-page', owner=admin_user)
        publish_page(ddp, bfp)

    if not LearnPage.objects.filter(title='Learn Page'):
        lp = LearnPage(title='Learn Page', slug='learn-page', owner=admin_user)
        publish_page(lp, bfp)
