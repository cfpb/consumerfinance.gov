from __future__ import print_function
import os
import sys

from elasticsearch.exceptions import NotFoundError

from django.db import models
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page, PagePermissionTester, UserPagePermissionsProxy, Orderable
from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from sheerlike.query import get_document, more_like_this
from . import ref


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

    # Settings for related posts on a page
    related_limit = models.IntegerField(default=3, verbose_name='Limit',
                                        help_text='Limits results per type.')
    is_relating_posts = models.BooleanField(default=True,
                                            verbose_name='Blog Posts')
    is_relating_newsroom = models.BooleanField(default=True,
                                               verbose_name='Newsroom')
    is_relating_events = models.BooleanField(default=True,
                                             verbose_name='Events')
    view_more_label = models.CharField(max_length=40, default='View More')
    view_more_url = models.CharField(max_length=200, blank=False,
                                     help_text='URL to additional related '
                                     + 'content.', default='/')

    # This is used solely for subclassing pages we want to make at the CFPB.
    is_creatable = False

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Page configuration"),
        FieldPanel('tags', 'Tags'),
        FieldPanel('authors', 'Authors'),
        InlinePanel('categories', label="Categories", max_num=2),
        MultiFieldPanel([
            FieldPanel('view_more_label', 'View More Label'),
            FieldPanel('view_more_url', 'View More URL'),
            FieldPanel('related_limit', 'Limit'),
            FieldRowPanel([
                FieldPanel('is_relating_posts', classname='col4'),
                FieldPanel('is_relating_newsroom', classname='col4'),
                FieldPanel('is_relating_events', classname='col4')
            ])
        ], heading='Related Posts')
    ]

    # TODO: After all search types are migrated to Wagtail this should relate
    # pages based on tags.
    @property
    def related_posts(self):
        # After all search types are migrated to Wagtail, comment out below. If
        # we decide we'd like to use the more_like_this feature of
        # Elasticsearch, we can always revert back to this.
        results = {}
        for search_type in ['posts', 'newsroom', 'events']:
            if getattr(self, 'is_relating_%s' % search_type):
                results.update({search_type: []})

        try:
            # Gets an ES document across all types by the slug of the page.
            document = get_document('_all', self.slug)
            for search_type in results.keys():
                results[search_type] = more_like_this(document,
                                                      search_types=search_type,
                                                      search_size=
                                                      self.related_limit)
        except NotFoundError:
            print('ES document not found for page.', file=sys.stderr)
        return results
        # Comment out above

        # TODO:After all search types are migrated to Wagtail, uncomment below.
        # query = Q(('tags__name__in', self.tags))
        # search_types = {
        #     'blog_posts': 'BlogPostPage',
        #     'newsroom_items': 'NewsroomPage',
        #     'events': 'EventPage',
        # }
        # related = []
        # for search_type in ['posts', 'newsroom', 'events']:
        #     if eval('self.is_relating_%s' % search_type):
        #         related += eval('%s.objects.filter(query)[:%s]' %
        #                         search_types[search_type],
        #                         self.related_limit)
        # return related

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
        """Return a queryset of the pages that this user has permission to share"""
        # Deal with the trivial cases first...
        if not self.user.is_active:
            return Page.objects.none()
        if self.user.is_superuser:
            return Page.objects.all()

        sharable_pages = Page.objects.none()

        for perm in self.permissions.filter(permission_type='share'):
            # User has share permission on any subpage of perm.page
            # (including perm.page itself).
            sharable_pages |= Page.objects.descendant_of(perm.page, inclusive=True)

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
        Return a CFGOVPagePermissionTester object defining what actions the user can perform on this page
        """
        user_perms = CFGOVUserPagePermissionsProxy(user)
        return user_perms.for_page(self)

    class Meta:
        app_label = 'v1'


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
