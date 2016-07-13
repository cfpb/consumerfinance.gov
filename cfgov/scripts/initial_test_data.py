import os, json

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from wagtail.wagtailcore.models import Page, Site

from scripts import _atomic_helpers as atomic
from v1.models.base import CFGOVPage
from v1.models.home_page import HomePage
from v1.models.landing_page import LandingPage
from v1.models.sublanding_page import SublandingPage
from v1.models.learn_page import EventPage, LearnPage, DocumentDetailPage
from v1.models.browse_page import BrowsePage
from v1.models.browse_filterable_page import BrowseFilterablePage, EventArchivePage, NewsroomLandingPage
from v1.models.sublanding_filterable_page import SublandingFilterablePage, ActivityLogPage
from v1.models.newsroom_page import NewsroomPage, LegacyNewsroomPage
from v1.models.blog_page import BlogPage, LegacyBlogPage
from v1.models.snippets import Contact
from wagtail.wagtailcore.blocks import StreamValue
from treebeard.exceptions import NodeAlreadySaved



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
        site_root = HomePage(title='CFGOV', slug='home-page', depth=2, owner=admin_user)
        site_root.live = True
        root.add_child(instance=site_root)
        latest = site_root.save_revision(user=admin_user, submitted_for_moderation=False)
        latest.save()
    else:
        site_root = site_root[0]

    # Setting new site root
    site = Site.objects.first()
    if site.root_page_id != site_root.id:
        site.port = 8000
        site.root_page_id = site_root.id
        site.save()
        content_site = Site(hostname='content.localhost', port=8000, root_page_id=site_root.id)
        content_site.save()

    def publish_page(child=None, root=site_root):
        try:
            root.add_child(instance=child)
        except NodeAlreadySaved:
            pass
        revision = child.save_revision(
            user=admin_user,
            submitted_for_moderation=False,
        )
        revision.publish()

    # Create snippets
    contact = Contact.objects.filter(heading='Test User')
    if not contact:
        contact = Contact(heading='Test User')
    else:
        contact = contact[0]
    contact.contact_info = StreamValue(contact.contact_info.stream_block,
        [
            atomic.contact_email,
            atomic.contact_phone,
            atomic.contact_address
        ], True)
    contact.save()

    # Create each Page Type
    lap = LandingPage.objects.filter(title='Landing Page')
    if not lap:
        lap = LandingPage(title='Landing Page', slug='landing-page', owner=admin_user)
    else:
        lap = lap[0]
    lap.content = StreamValue(lap.content.stream_block,
        [
            atomic.image_text_25_75_group,
            atomic.image_text_50_50_group,
            atomic.half_width_link_blob_group,
            atomic.well
        ], True)
    lap.sidefoot = StreamValue(lap.sidefoot.stream_block,
        [
            atomic.related_links,
            atomic.sidebar_contact(contact.id)
        ], True)
    publish_page(lap)

    sp = SublandingPage.objects.filter(title='Sublanding Page')
    if not sp:
        sp = SublandingPage(title='Sublanding Page', slug='sublanding-page', owner=admin_user)
    else:
        sp = sp[0]
    sp.content = StreamValue(sp.content.stream_block,
        [
            atomic.main_contact_info(contact.id),
            atomic.reg_comment
        ], True)
    sp.sidefoot = StreamValue(sp.sidefoot.stream_block,
        [
            atomic.email_signup,
            atomic.rss_feed
        ], True)

    publish_page(sp)

    bp = BrowsePage.objects.filter(title='Browse Page')
    if not bp:
        bp = BrowsePage(title='Browse Page', slug='browse-page', owner=admin_user)
    else:
        bp = bp[0]
    bp.header = StreamValue(bp.header.stream_block,
        [
            atomic.featured_content
        ], True)
    bp.content = StreamValue(bp.content.stream_block,
        [
            atomic.expandable,
            atomic.expandable_group
        ], True)
    publish_page(bp)

    # Filterable Pages
    bfp = BrowseFilterablePage.objects.filter(title='Browse Filterable Page')
    if not bfp:
        bfp = BrowseFilterablePage(title='Browse Filterable Page', slug='browse-filterable-page', owner=admin_user)
    else:
        bfp = bfp[0]
    bfp.header = StreamValue(bfp.header.stream_block, [atomic.text_introduction], True)
    publish_page(bfp)

    sfp = SublandingFilterablePage.objects.filter(title='Sublanding Filterable Page')
    if not sfp:
        sfp = SublandingFilterablePage(title='Sublanding Filterable Page', slug='sublanding-filterable-page',
                                       owner=admin_user)
    else:
        sfp = sfp[0]
    sfp.header = StreamValue(sfp.header.stream_block, [atomic.hero], True)
    publish_page(sfp)

    eap = EventArchivePage.objects.filter(title='Event Archive Page')
    if not eap:
        eap = EventArchivePage(title='Event Archive Page', slug='event-archive-page', owner=admin_user)
    else:
        eap = eap[0]
    publish_page(eap)

    nlp = NewsroomLandingPage.objects.filter(title='Newsroom Landing Page')
    if not nlp:
        nlp = NewsroomLandingPage(title='Newsroom Landing Page', slug='newsroom-landing-page', owner=admin_user)
    else:
        nlp = nlp[0]
    publish_page(nlp)

    alp = ActivityLogPage.objects.filter(title='Activity Log Page')
    if not alp:
        alp = ActivityLogPage(title='Activity Log Page', slug='activity-log-page', owner=admin_user)
    else:
        alp = alp[0]
    publish_page(alp)

    # Filter Pages
    if not EventPage.objects.filter(title='Event Page'):
        ep = EventPage(title='Event Page', slug='event-page', owner=admin_user)
        publish_page(ep, bfp)

    ddp = DocumentDetailPage.objects.filter(title='Document Detail Page')
    if not ddp:
        ddp = DocumentDetailPage(title='Document Detail Page', slug='document-detail-page', owner=admin_user)
    else:
        ddp = ddp[0]
    ddp.sidefoot = StreamValue(ddp.sidefoot.stream_block, [atomic.related_metadata], True)
    publish_page(ddp, bfp)

    lp = LearnPage.objects.filter(title='Learn Page')
    if not lp:
        lp = LearnPage(title='Learn Page', slug='learn-page', owner=admin_user)
    else:
        lp = lp[0]
    lp.header = StreamValue(lp.header.stream_block, [atomic.item_introduction], True)
    lp.content = StreamValue(lp.content.stream_block,
        [
            atomic.full_width_text,
            atomic.call_to_action,
            atomic.table
        ], True)
    publish_page(lp, bfp)

    if not NewsroomPage.objects.filter(title='Newsroom Page'):
        np = NewsroomPage(title='Newsroom Page', slug='newsroom-page', owner=admin_user)
        publish_page(np, nlp)

    if not LegacyNewsroomPage.objects.filter(title='Legacy Newsroom Page'):
        lnp = LegacyNewsroomPage(title='Legacy Newsroom Page', slug='legacy-newsroom-page', owner=admin_user)
        publish_page(lnp, nlp)

    if not BlogPage.objects.filter(title='Blog Page'):
        bp = BlogPage(title='Blog Page', slug='blog-page', owner=admin_user)
        publish_page(bp, sfp)

    if not LegacyBlogPage.objects.filter(title='Legacy Blog Page'):
        lbp = LegacyBlogPage(title='Legacy Blog Page', slug='legacy-blog-page', owner=admin_user)
        publish_page(lbp, sfp)


    # Create and configure pages for testing page states
    draft = LandingPage.objects.filter(slug='draft-page')
    if not draft:
        draft = LandingPage(title='Draft Page', slug='draft-page', owner=admin_user, live=False, shared=False)
        site_root.add_child(instance=draft)
    else:
        draft = draft[0]
    draft.save_revision(user=admin_user)

    shared = LandingPage.objects.filter(slug='shared-page')
    if not shared:
        shared = LandingPage(title='Shared Page', slug='shared-page', owner=admin_user, live=False, shared=True)
        site_root.add_child(instance=shared)
    else:
        shared = shared[0]
    shared.save_revision(user=admin_user)

    shared_draft = LandingPage.objects.filter(slug='shared-draft-page')
    if not shared_draft:
        shared_draft = LandingPage(title='Shared Page', slug='shared-draft-page', owner=admin_user, live=False, shared=True)
        site_root.add_child(instance=shared_draft)
    else:
        shared_draft = shared_draft[0]
    shared_draft.save_revision(user=admin_user)
    shared_draft.title = 'Shared Draft Page'
    shared_draft.shared = False
    shared_draft.save()
    shared_draft.save_revision(user=admin_user)

    live = LandingPage.objects.filter(slug='live-page')
    if not live:
        live = LandingPage(title='Live Page', slug='live-page', owner=admin_user, live=True, shared=True)
    else:
        live = live[0]
    publish_page(live)

    livedraft = LandingPage.objects.filter(slug='live-draft-page')
    if not livedraft:
        livedraft = LandingPage(title='Live Draft Page', slug='live-draft-page', owner=admin_user, live=True, shared=True)
    else:
        livedraft = livedraft[0]
    publish_page(livedraft)
    livedraft.live = False
    livedraft.shared = False
    livedraft.title = 'Live Page'
    livedraft.save_revision(user=admin_user)
