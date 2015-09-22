from django.db import models
from django.http import Http404

from cfgov.settings.base import STAGING_HOSTNAME

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.url_routing import RouteResult
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from django.utils.translation import ugettext_lazy as _


class V1Page(Page):
    is_sharable = models.BooleanField(default=False)

    # This is used solely for subclassing page's we want to make at the CFPB
    is_creatable = False

    @property
    def status_string(self):
        if not self.live:
            if self.expired:
                return _("expired")
            elif self.approved_schedule:
                return _("scheduled")
            elif self.is_sharable:
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
            if self.live or self.is_sharable and request.site.hostname == STAGING_HOSTNAME:
                return RouteResult(self)
            else:
                print "here"
                raise Http404


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
