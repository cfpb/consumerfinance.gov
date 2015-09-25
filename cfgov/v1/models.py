from django.db import models
from django.http import Http404
from django.conf import settings

from wagtail.wagtailcore.models import Page, PagePermissionTester, UserPagePermissionsProxy
from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from django.utils.translation import ugettext_lazy as _


class V1Page(Page):
    shared = models.BooleanField(default=False)

    # This is used solely for subclassing page's we want to make at the CFPB
    is_creatable = False

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
            # user has share permission on any subpage of perm.page
            # (including perm.page itself)
            sharable_pages |= Page.objects.descendant_of(perm.page, inclusive=True)

        return sharable_pages

    def can_share_pages(self):
        """Return True if the user has permission to publish any pages"""
        return self.sharable_pages().exists()

    def route(self, request, path_components):
        if path_components:
            # request is for a child of this page
            child_slug = path_components[0]
            remaining_components = path_components[1:]

            try:
                subpage = self.get_children().get(slug=child_slug)
            except Page.DoesNotExist:
                raise Http404

            return subpage.specific.route(request, remaining_components)

        else:
            # request is for this very page
            if self.live or self.shared and request.site.hostname == settings.STAGING_HOSTNAME:
                return RouteResult(self)
            else:
                raise Http404

    def permissions_for_user(self, user):
        """
        Return a V1PagePermissionsTester object defining what actions the user can perform on this page
        """
        user_perms = V1UserPagePermissionsProxy(user)
        return user_perms.for_page(self)


class V1PagePermissionTester(PagePermissionTester):
    def can_unshare(self):
        if not self.user.is_active:
            return False
        if not self.page.shared or self.page_is_root:
            return False

        # Must check edit in self.permissions because `share` cannot be added
        return self.user.is_superuser or ('edit' in self.permissions)

    def can_share(self):
        if not self.user.is_active:
            return False
        if self.page_is_root:
            return False

        # Must check edit in self.permissions because `share` cannot be added
        return self.user.is_superuser or ('edit' in self.permissions)


class V1UserPagePermissionsProxy(UserPagePermissionsProxy):
    def for_page(self, page):
        """Return a V1PagePermissionTester object that can be used to query
            whether this user has permission to perform specific tasks on the
            given page."""
        return V1PagePermissionTester(self, page)


class BlogPage(V1Page):
    body = RichTextField()
    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname="full"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]
