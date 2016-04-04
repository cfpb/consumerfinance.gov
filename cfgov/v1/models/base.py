import os
import json
from itertools import chain
from collections import OrderedDict

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User

from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks.stream_block import StreamValue
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page, PagePermissionTester, \
    UserPagePermissionsProxy, Orderable, PageManager, PageQuerySet
from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, \
    MultiFieldPanel, TabbedInterface, ObjectList
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from sheerlike.query import QueryFinder

from . import molecules
from . import organisms
from ..util import util, ref

import urllib


class CFGOVAuthoredPages(TaggedItemBase):
    content_object = ParentalKey('CFGOVPage')

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class CFGOVTaggedPages(TaggedItemBase):
    content_object = ParentalKey('CFGOVPage')

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class CFGOVPageQuerySet(PageQuerySet):
    def shared_q(self):
        return Q(shared=True)

    def shared(self):
        return self.filter(self.shared_q())

    def live_shared_q(self):
        return self.live_q() | self.shared_q()

    def live_shared(self, hostname):
        staging_hostname = os.environ.get('STAGING_HOSTNAME')
        if staging_hostname in hostname:
            return self.filter(self.live_shared_q())
        else:
            return self.live()


class BaseCFGOVPageManager(PageManager):
    def get_queryset(self):
        return CFGOVPageQuerySet(self.model).order_by('path')

CFGOVPageManager = BaseCFGOVPageManager.from_queryset(CFGOVPageQuerySet)


class CFGOVPage(Page):
    authors = ClusterTaggableManager(through=CFGOVAuthoredPages, blank=True,
                                     verbose_name='Authors',
                                     help_text='A comma separated list of '
                                               + 'authors.',
                                     related_name='authored_pages')
    tags = ClusterTaggableManager(through=CFGOVTaggedPages, blank=True,
                                  related_name='tagged_pages')
    shared = models.BooleanField(default=False)

    language = models.CharField(choices=ref.supported_languagues, default='en', max_length=2)

    # This is used solely for subclassing pages we want to make at the CFPB.
    is_creatable = False

    objects = CFGOVPageManager()

    # These fields show up in either the sidebar or the footer of the page
    # depending on the page type.
    sidefoot = StreamField([
        ('call_to_action', molecules.CallToAction()),
        ('related_links', molecules.RelatedLinks()),
        ('related_posts', organisms.RelatedPosts()),
        ('related_metadata', molecules.RelatedMetadata()),
        ('email_signup', organisms.EmailSignUp()),
        ('contact', organisms.MainContactInfo()),
        ('sidebar_contact', organisms.SidebarContactInfo()),
    ], blank=True)

    # Panels
    sidefoot_panels = [
        StreamFieldPanel('sidefoot'),
    ]

    settings_panels = [
        MultiFieldPanel(Page.promote_panels, 'Settings'),
        FieldPanel('tags', 'Tags'),
        FieldPanel('authors', 'Authors'),
        FieldPanel('language', 'language'),
        InlinePanel('categories', label="Categories", max_num=2),
        MultiFieldPanel(Page.settings_panels, 'Scheduled Publishing'),
    ]

    # Tab handler interface guide because it must be repeated for each subclass
    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='Sidebar/Footer'),
        ObjectList(settings_panels, heading='Configuration'),
    ])

    def generate_view_more_url(self):
        url = '/activity-log/?'
        tags = []
        for tag in self.tags.names():
            tags.append('filter_tags=' + urllib.quote_plus(tag))
        tags = '&'.join(tags)
        return url + tags

    def related_posts(self, block, hostname):
        related = {}
        query = models.Q(('tags__name__in', self.tags.names()))
        block.value['view_more']['text'] = "View more"
        if self.tags.names():
            block.value['view_more']['url'] = self.generate_view_more_url()
            self.save()
        # TODO: Add other search types as they are implemented in Django
        # Import classes that use this class here to maintain proper import
        # order.
        from . import EventPage
        search_types = [
            ('events', EventPage, 'Events'),
        ]
        for search_type, search_class, search_type_name in search_types:
            if 'relate_%s' % search_type in block.value \
                    and block.value['relate_%s' % search_type]:
                related[search_type_name] = \
                    search_class.objects.filter(query).order_by(
                        '-date_published').exclude(
                        slug=self.slug).live_shared(hostname)[:block.value['limit']]
        # TODO: Remove each search_type as it is implemented into Django
        queries = QueryFinder()

        for search_type, search_type_name in [('newsroom', 'Newsroom'), ('posts', 'Blog')]:
            if 'relate_%s' % search_type in block.value \
                    and block.value['relate_%s' % search_type]:
                if search_type == 'newsroom':
                    search_type = 'just_newsroom'
                sheer_query = getattr(queries, search_type)

                match_query = []

                for cat in block.value['specific_categories']:
                    if util.get_related_posts_categories(cat) == 'posts' and search_type == 'posts':
                        match_query.append({'term': {'blog_category': cat}})
                    elif util.get_related_posts_categories(cat) == 'newsroom' and search_type == 'just_newsroom':
                        match_query.append({'term': {'category': cat}})

                related[search_type_name] = \
                    sheer_query.get_tag_related_documents(tags=self.tags.names(),
                                                          size=block.value['limit'], additional_args=match_query)

        # Return a dictionary of lists of each type when there's at least one
        # hit for that type.
        return {search_type: queryset for search_type, queryset in
                related.items() if queryset}

    def get_breadcrumbs(self, site):
        ancestors = self.get_ancestors()
        home_page_children = site.root_page.get_children()
        for i, ancestor in enumerate(ancestors):
            if ancestor in home_page_children:
                return ancestors[i+1:]
        return []

    def get_appropriate_descendants(self, hostname, inclusive=True):
        return CFGOVPage.objects.live_shared(hostname).descendant_of(self, inclusive)

    def get_appropriate_siblings(self, hostname, inclusive=True):
        return CFGOVPage.objects.live_shared(hostname).sibling_of(self, inclusive)

    def get_next_appropriate_siblings(self, hostname, inclusive=False):
        return self.get_appropriate_siblings(hostname=hostname, inclusive=inclusive).filter(path__gte=self.path).order_by('path')

    def get_prev_appropriate_siblings(self, hostname, inclusive=False):
        return self.get_appropriate_siblings(hostname=hostname, inclusive=inclusive).filter(path__lte=self.path).order_by('-path')

    @property
    def status_string(self):
        if not self.live:
            if self.expired:
                return _("expired")
            elif self.approved_schedule:
                return _("scheduled")
            elif self.shared:
                return _("shared")
            else:
                return _("draft")
        else:
            if self.has_unpublished_changes:
                return _("live + draft")
            else:
                return _("live")

    def sharable_pages(self):
        """
        Return a queryset of the pages that this user has permission to share.
        """
        # Deal with the trivial cases first...
        if not self.user.is_active:
            return Page.objects.none()
        if self.user.is_superuser:
            return Page.objects.all()

        sharable_pages = Page.objects.none()

        for perm in self.permissions.filter(permission_type='share'):
            # User has share permission on any subpage of perm.page
            # (including perm.page itself).
            sharable_pages |= Page.objects.descendant_of(perm.page,
                                                         inclusive=True)

        return sharable_pages

    def can_share_pages(self):
        """Return True if the user has permission to publish any pages"""
        return self.sharable_pages().exists()

    def route(self, request, path_components):
        if path_components:
            # Request is for a child of this page.
            child_slug = path_components[0]
            remaining_components = path_components[1:]

            try:
                subpage = self.get_children().get(slug=child_slug)
            except Page.DoesNotExist:
                raise Http404

            return subpage.specific.route(request, remaining_components)

        else:
            # Request is for this very page.
            # If we're on the production site, make sure the version of the page
            # displayed is the latest version that has `live` set to True for
            # the live site or `shared` set to True for the staging site.
            staging_hostname = os.environ.get('STAGING_HOSTNAME')
            revisions = self.revisions.all().order_by('-created_at')
            for revision in revisions:
                page_version = json.loads(revision.content_json)
                if request.site.hostname != staging_hostname:
                    if page_version['live']:
                        return RouteResult(revision.as_page_object())
                else:
                    if page_version['shared']:
                        return RouteResult(revision.as_page_object())
            raise Http404

    def permissions_for_user(self, user):
        """
        Return a CFGOVPagePermissionTester object defining what actions the
        user can perform on this page
        """
        user_perms = CFGOVUserPagePermissionsProxy(user)
        return user_perms.for_page(self)

    class Meta:
        app_label = 'v1'

    def parent(self):
        parent = self.get_ancestors(inclusive=False).reverse()[0].specific
        return parent

    # To be overriden if page type requires JS files every time
    # 'template' is used as the key for front-end consistency
    def add_page_js(self, js):
        js['template'] = []

    # Retrieves the stream values on a page from it's Streamfield
    def _get_streamfield_blocks(self):
        lst = [value for key, value in vars(self).iteritems()
               if type(value) is StreamValue]
        return list(chain(*lst))

    # Gets the JS from the Streamfield data
    def _add_streamfield_js(self, js):
        # Create a dictionary with keys ordered organisms, molecules, then atoms
        for child in self._get_streamfield_blocks():
            self._add_block_js(child.block, js)

    # Recursively search the blocks and classes for declared Media.js
    def _add_block_js(self, block, js):
        self._assign_js(block, js)
        if issubclass(type(block), blocks.StructBlock):
            for child in block.child_blocks.values():
                self._add_block_js(child, js)
        elif issubclass(type(block), blocks.ListBlock):
            self._add_block_js(block.child_block, js)

    # Assign the Media js to the dictionary appropriately
    def _assign_js(self, obj, js):
        try:
            if hasattr(obj.Media, 'js'):
                for key in js.keys():
                    if obj.__module__.endswith(key):
                        js[key] += obj.Media.js
                if not [key for key in js.keys() if obj.__module__.endswith(key)]:
                    js.update({'other': obj.Media.js})
        except:
            pass

    # Returns all the JS files specific to this page and it's current Streamfield's blocks
    @property
    def media(self):
        js = OrderedDict()
        for key in ['template', 'organisms', 'molecules', 'atoms']:
            js.update({key: []})
        self.add_page_js(js)
        self._add_streamfield_js(js)
        for key, js_files in js.iteritems():
            js[key] = list(set(js_files))
        return js


class CFGOVPageCategory(Orderable):
    page = ParentalKey(CFGOVPage, related_name='categories')
    name = models.CharField(max_length=255, choices=ref.categories)

    panels = [
        FieldPanel('name'),
    ]


class CFGOVPagePermissionTester(PagePermissionTester):
    def can_unshare(self):
        if not self.user.is_active:
            return False
        if not self.page.shared or self.page_is_root:
            return False

        # Must check edit in self.permissions because `share` cannot be added.
        return self.user.is_superuser or ('edit' in self.permissions)

    def can_share(self):
        if not self.user.is_active:
            return False
        if self.page_is_root:
            return False

        # Must check edit in self.permissions because `share` cannot be added.
        return self.user.is_superuser or ('edit' in self.permissions)


class CFGOVUserPagePermissionsProxy(UserPagePermissionsProxy):
    def for_page(self, page):
        """Return a CFGOVPagePermissionTester object that can be used to query
            whether this user has permission to perform specific tasks on the
            given page."""
        return CFGOVPagePermissionTester(self, page)


class CFGOVImage(AbstractImage):
    alt = models.CharField(max_length=100, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'alt',
    )


class CFGOVRendition(AbstractRendition):
    image = models.ForeignKey(CFGOVImage, related_name='renditions')


# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=CFGOVImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=CFGOVRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)

# keep encrypted passwords around to ensure that user does not re-use any of the
# previous 10
class PasswordHistoryItem(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()   # password becomes invalid at...
    locked_until = models.DateTimeField() # password can not be changed until...
    encrypted_password = models.CharField(_('password'), max_length=128)

    class Meta:
        get_latest_by = 'created'

    @classmethod
    def current_for_user(cls,user):
        return user.passwordhistoryitem_set.latest()
        
    def can_change_password(self):
        now = timezone.now()
        return(now > self.locked_until)

    def must_change_password(self):
        now = timezone.now()
        return(self.expires_at < now)

# User Failed Login Attempts
class FailedLoginAttempt(models.Model):
    user = models.OneToOneField(User)
    # comma-separated timestamp values, right now it's a 10 digit number,
    # so we can store about 91 last failed attempts
    failed_attempts = models.CharField(max_length=1000)

    def __unicode__(self):
        attempts_no = 0 if not self.failed_attempts else len(self.failed_attempts.split(','))
        return "%s has %s failed login attempts" % (self.user, attempts_no)

    def clean_attempts(self, timestamp):
        """ Leave only those that happened after <timestamp> """
        attempts = self.failed_attempts.split(',')
        self.failed_attempts = ','.join([fa for fa in attempts if int(fa) >= timestamp])

    def failed(self, timestamp):
        """ Add another failed attempt """
        attempts = self.failed_attempts.split(',') if self.failed_attempts else []
        attempts.append(str(int(timestamp)))
        self.failed_attempts = ','.join(attempts)

    def too_many_attempts(self, value, timestamp):
        """ Compare number of failed attempts to <value> """
        self.clean_attempts(timestamp)
        attempts = self.failed_attempts.split(',')
        return len(attempts) > value

class TemporaryLockout(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
