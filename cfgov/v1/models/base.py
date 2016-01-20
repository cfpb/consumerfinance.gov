import os

from django.db import models
from django.db.models.signals import pre_delete
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.contrib.auth.models import User

from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page, PagePermissionTester, \
    UserPagePermissionsProxy, Orderable
from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, \
    MultiFieldPanel, TabbedInterface, ObjectList

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from sets import Set

from . import ref
from . import atoms
from . import molecules
from . import organisms
from ..util import util


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


class CFGOVPage(Page):
    authors = ClusterTaggableManager(through=CFGOVAuthoredPages, blank=True,
                                     verbose_name='Authors',
                                     help_text='A comma separated list of '
                                               + 'authors.',
                                     related_name='authored_pages')
    tags = ClusterTaggableManager(through=CFGOVTaggedPages, blank=True,
                                  related_name='tagged_pages')
    shared = models.BooleanField(default=False)

    # This is used solely for subclassing pages we want to make at the CFPB.
    is_creatable = False

    # These fields show up in either the sidebar or the footer of the page
    # depending on the page type.
    sidefoot = StreamField([
        ('slug', blocks.CharBlock(icon='title')),
        ('heading', blocks.CharBlock(icon='title')),
        ('paragraph', blocks.TextBlock(icon='edit')),
        ('hyperlink', atoms.Hyperlink()),
        ('call_to_action', molecules.CallToAction()),
        ('related_links', molecules.RelatedLinks()),
        ('related_posts', organisms.RelatedPosts()),
        ('email_signup', organisms.EmailSignUp()),
        ('contact', organisms.MainContactInfo()),
    ], blank=True)

    # Panels
    sidefoot_panels = [
        StreamFieldPanel('sidefoot'),
    ]

    settings_panels = [
        MultiFieldPanel(Page.promote_panels, 'Settings'),
        FieldPanel('tags', 'Tags'),
        FieldPanel('authors', 'Authors'),
        InlinePanel('categories', label="Categories", max_num=2),
        MultiFieldPanel(Page.settings_panels, 'Scheduled Publishing'),
    ]

    # Tab handler interface guide because it must be repeated for each subclass
    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='Sidebar/Footer'),
        ObjectList(settings_panels, heading='Configuration'),
    ])

    def related_posts(self, block):
        related = {}
        query = models.Q(('tags__name__in', self.tags.names()))
        # TODO: Replace this in a more global scope when Filterable List gets
        # implemented in the backend.
        # Import classes that use this class here to maintain proper import
        # order.
        from . import EventPage
        search_types = {
            'events': EventPage,
        }
        # End TODO
        for search_type, page_class in search_types.items():
            if 'relate_%s' % search_type in block.value \
                    and block.value['relate_%s' % search_type]:
                related[search_type] = \
                    page_class.objects.filter(query).order_by(
                        '-latest_revision_created_at').exclude(
                        slug=self.slug)[:block.value['limit']]

        # Return a dictionary of lists of each type when there's at least one
        # hit for that type.
        return {search_type: queryset for search_type, queryset in
                related.items() if queryset}

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
            if self.live or self.shared and request.site.hostname == \
                    os.environ.get('STAGING_HOSTNAME'):
                return RouteResult(self)
            else:
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

    def elements(self):
        return []

    def _media(self):
        from v1 import models

        js = ()

        for child in self.elements():
            if isinstance(child, dict):
                type = child['type']
            else:
                type = child[0]

            class_ = getattr(models, util.to_camel_case(type))

            instance = class_()

            try:
                if hasattr(instance.Media, 'js'):
                    js += instance.Media.js
            except:
                pass

        return Set(js)

    media = property(_media)


class CFGOVPageCategory(Orderable):
    page = ParentalKey(CFGOVPage, related_name='categories')
    name = models.CharField(max_length=255, choices=ref.choices)

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
