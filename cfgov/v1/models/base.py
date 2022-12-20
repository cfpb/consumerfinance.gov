import re

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Value
from django.utils import timezone, translation
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Site
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import ItemBase, TagBase, TaggedItemBase
from wagtailinventory.helpers import get_page_blocks

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.banners import Banner
from v1.models.snippets import ReusableText
from v1.util import ref
from v1.util.util import validate_social_sharing_image


class CFGOVAuthoredPages(TaggedItemBase):
    content_object = ParentalKey("CFGOVPage")

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class CFGOVTaggedPages(TaggedItemBase):
    content_object = ParentalKey("CFGOVPage")

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class CFGOVContentOwner(TagBase):
    class Meta:
        verbose_name = _("Content Owner")
        verbose_name_plural = _("Content Owners")


class CFGOVOwnedPages(ItemBase):
    tag = models.ForeignKey(
        CFGOVContentOwner, related_name="owned_pages", on_delete=models.CASCADE
    )
    content_object = ParentalKey("CFGOVPage")


class CFGOVPage(Page):
    authors = ClusterTaggableManager(
        through=CFGOVAuthoredPages,
        blank=True,
        verbose_name="Authors",
        help_text="A comma separated list of " + "authors.",
        related_name="authored_pages",
    )
    tags = ClusterTaggableManager(
        through=CFGOVTaggedPages, blank=True, related_name="tagged_pages"
    )
    language = models.CharField(
        choices=settings.LANGUAGES, default="en", max_length=100
    )
    social_sharing_image = models.ForeignKey(
        "v1.CFGOVImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=(
            "Optionally select a custom image to appear when users share this "
            "page on social media websites. Recommended size: 1200w x 630h. "
            "Maximum size: 4096w x 4096h."
        ),
    )

    content_owners = ClusterTaggableManager(
        through=CFGOVOwnedPages,
        blank=True,
        verbose_name="Content Owners",
        help_text="A comma separated list of internal content owners."
        + "Use division acronyms only.",
        related_name="cfgov_content_owners",
    )

    schema_json = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Schema JSON",
        help_text=mark_safe(
            "Enter structured data for this page in JSON-LD format, "
            "for use by search engines in providing rich search results. "
            '<a href="https://developers.google.com/search/docs/guides/'
            'intro-structured-data">Learn more.</a> '
            "JSON entered here will be output in the "
            "<code>&lt;head&gt;</code> of the page between "
            '<code>&lt;script type="application/ld+json"&gt;</code> and '
            "<code>&lt;/script&gt;</code> tags."
        ),
    )
    force_breadcrumbs = models.BooleanField(
        "Force breadcrumbs on child pages",
        default=False,
        blank=True,
        help_text=(
            "Normally breadcrumbs don't appear on pages one or two levels "
            "below the homepage. Check this option to force breadcrumbs to "
            "appear on all children of this page no matter how many levels "
            "below the homepage they are (for example, if you want "
            "breadcrumbs to appear on all children of a top-level campaign "
            "page)."
        ),
    )

    # This is used solely for subclassing pages we want to make at the CFPB.
    is_creatable = False

    # These fields show up in either the sidebar or the footer of the page
    # depending on the page type.
    sidefoot = StreamField(
        [
            ("call_to_action", molecules.CallToAction()),
            ("related_links", molecules.RelatedLinks()),
            ("related_posts", organisms.RelatedPosts()),
            ("related_metadata", molecules.RelatedMetadata()),
            (
                "email_signup",
                v1_blocks.EmailSignUpChooserBlock(),
            ),
            ("sidebar_contact", organisms.SidebarContactInfo()),
            ("rss_feed", molecules.RSSFeed()),
            ("social_media", molecules.SocialMedia()),
            (
                "reusable_text",
                v1_blocks.ReusableTextChooserBlock(ReusableText),
            ),
        ],
        blank=True,
    )

    # Panels
    promote_panels = Page.promote_panels + [
        ImageChooserPanel("social_sharing_image"),
        FieldPanel("force_breadcrumbs", "Breadcrumbs"),
    ]

    sidefoot_panels = [
        StreamFieldPanel("sidefoot"),
    ]

    settings_panels = [
        MultiFieldPanel(promote_panels, "Settings"),
        InlinePanel("categories", label="Categories", max_num=2),
        FieldPanel("tags", "Tags"),
        FieldPanel("authors", "Authors"),
        FieldPanel("content_owners", "Content Owners"),
        FieldPanel("schema_json", "Structured Data"),
        MultiFieldPanel(Page.settings_panels, "Scheduled Publishing"),
        FieldPanel("language", "language"),
    ]

    # Tab handler interface guide because it must be repeated for each subclass
    edit_handler = TabbedInterface(
        [
            ObjectList(Page.content_panels, heading="General Content"),
            ObjectList(sidefoot_panels, heading="Sidebar/Footer"),
            ObjectList(settings_panels, heading="Configuration"),
        ]
    )

    default_exclude_fields_in_copy = Page.default_exclude_fields_in_copy + [
        "tags",
        "authors",
    ]

    def clean(self):
        super().clean()
        validate_social_sharing_image(self.social_sharing_image)

    def get_authors(self):
        """Returns a sorted list of authors. Default is alphabetical"""
        return self.alphabetize_authors()

    def alphabetize_authors(self):
        """
        Alphabetize authors of this page by last name,
        then first name if needed
        """
        # First sort by first name
        author_names = self.authors.order_by("name")
        # Then sort by last name
        return sorted(author_names, key=lambda x: x.name.split()[-1])

    def is_faq_block(self, item):
        return item.block_type == "faq_group" or (
            item.block_type == "expandable_group"
            and item.value["is_faq"] is True
        )

    def is_faq_page(self):
        if hasattr(self, "content"):
            return any(self.is_faq_block(item) for item in self.content)

    def related_metadata_tags(self):
        # Set the tags to correct data format
        tags = {"links": []}
        filter_page = self.get_filter_data()
        for tag in self.specific.tags.all():
            tag_link = {"text": tag.name, "url": ""}
            if filter_page:
                relative_url = filter_page.relative_url(filter_page.get_site())
                param = "?topics=" + tag.slug
                tag_link["url"] = relative_url + param
            tags["links"].append(tag_link)
        return tags

    def get_filter_data(self):
        for ancestor in self.get_ancestors().reverse().specific():
            if ancestor.specific_class.__name__ in [
                "BrowseFilterablePage",
                "SublandingFilterablePage",
                "EventArchivePage",
                "NewsroomLandingPage",
            ]:
                return ancestor
        return None

    def get_breadcrumbs(self, request):
        ancestors = self.get_ancestors().specific()
        site = Site.find_for_request(request)
        for i, ancestor in enumerate(ancestors):
            if ancestor.is_child_of(site.root_page):
                if ancestor.specific.force_breadcrumbs:
                    return ancestors[i:]
                return ancestors[i + 1 :]
        return []

    def get_appropriate_descendants(self, inclusive=True):
        return CFGOVPage.objects.live().descendant_of(self, inclusive)

    def get_appropriate_siblings(self, inclusive=True):
        return CFGOVPage.objects.live().sibling_of(self, inclusive)

    def remove_html_tags(self, text):
        clean = re.compile("<.*?>")
        return re.sub(clean, " ", text)

    def get_streamfield_content(self, section, blockType, value):
        for item in section:
            if item.block_type is blockType:
                return self.remove_html_tags(item.value[value].source)
        return

    def get_meta_description(self):
        """Determine what the page's meta and OpenGraph description should be

        Checks several different possible fields in order of preference.
        If none are found, returns an empty string, which is preferable to a
        generic description repeated on many pages.
        """

        preference_order = [
            "search_description",
            "header_hero_body",
            "preview_description",
            "header_text_intro",
            "content_text_intro",
            "header_item_intro",
        ]
        candidates = {}

        if self.search_description:
            candidates["search_description"] = self.search_description
        if hasattr(self, "header"):
            candidates["header_hero_body"] = self.get_streamfield_content(
                self.header, "hero", "body"
            )
            candidates["header_text_intro"] = self.get_streamfield_content(
                self.header, "text_introduction", "intro"
            )
            candidates["header_item_intro"] = self.get_streamfield_content(
                self.header, "item_introduction", "paragraph"
            )
        if hasattr(self, "preview_description") and self.preview_description:
            candidates["preview_description"] = self.remove_html_tags(
                self.preview_description
            )
        if hasattr(self, "content"):
            candidates["content_text_intro"] = self.get_streamfield_content(
                self.content, "text_introduction", "intro"
            )

        for entry in preference_order:
            if candidates.get(entry):
                return candidates[entry]

        return ""

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Add any banners that are enabled and match the current request path
        # to a context variable.
        context["banners"] = (
            Banner.objects.filter(enabled=True)
            .annotate(
                # This annotation creates a path field in the QuerySet
                # that we can use in the filter below to compare with
                # the url_pattern defined on each enabled banner.
                path=Value(request.path, output_field=models.CharField())
            )
            .filter(path__regex=F("url_pattern"))
        )

        if self.schema_json:
            context["schema_json"] = self.schema_json

        context["meta_description"] = self.get_meta_description()
        context["is_faq_page"] = self.is_faq_page()
        return context

    def serve(self, request, *args, **kwargs):
        # Force the page's language on the request
        translation.activate(self.language)
        request.LANGUAGE_CODE = translation.get_language()
        return super().serve(request, *args, **kwargs)

    def streamfield_media(self, media_type):
        media = []

        block_cls_names = get_page_blocks(self)
        for block_cls_name in block_cls_names:
            block_cls = import_string(block_cls_name)
            if hasattr(block_cls, "Media") and hasattr(
                block_cls.Media, media_type
            ):
                media.extend(getattr(block_cls.Media, media_type))

        return media

    # To be overriden if page type requires JS files every time
    @property
    def page_js(self):
        return []

    # Returns the JS files required by this page and its StreamField blocks.
    @property
    def media_js(self):
        return sorted(set(self.page_js + self.streamfield_media("js")))

    # Returns the CSS files required by this page and its StreamField blocks.
    @property
    def media_css(self):
        return sorted(set(self.streamfield_media("css")))

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        return self.social_sharing_image

    @property
    def post_preview_cache_key(self):
        return "post_preview_{}".format(self.id)


class CFGOVPageCategory(models.Model):
    page = ParentalKey(CFGOVPage, related_name="categories")
    name = models.CharField(max_length=255, choices=ref.categories)

    class Meta:
        ordering = ["name"]

    panels = [
        FieldPanel("name"),
    ]


# keep encrypted passwords around to ensure that user does not re-use
# any of the previous 10
class PasswordHistoryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # password becomes invalid at...
    locked_until = models.DateTimeField()  # password cannot be changed until
    encrypted_password = models.CharField(_("password"), max_length=128)

    class Meta:
        get_latest_by = "created"

    @classmethod
    def current_for_user(cls, user):
        return user.passwordhistoryitem_set.latest()

    def can_change_password(self):
        now = timezone.now()
        return now > self.locked_until

    def must_change_password(self):
        now = timezone.now()
        return self.expires_at < now


# User Failed Login Attempts
class FailedLoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # comma-separated timestamp values, right now it's a 10 digit number,
    # so we can store about 91 last failed attempts
    failed_attempts = models.CharField(max_length=1000)

    def __unicode__(self):
        attempts_no = (
            0
            if not self.failed_attempts
            else len(self.failed_attempts.split(","))
        )
        return "%s has %s failed login attempts" % (self.user, attempts_no)

    def clean_attempts(self, timestamp):
        """Leave only those that happened after <timestamp>"""
        attempts = self.failed_attempts.split(",")
        self.failed_attempts = ",".join(
            [fa for fa in attempts if int(fa) >= timestamp]
        )

    def failed(self, timestamp):
        """Add another failed attempt"""
        attempts = (
            self.failed_attempts.split(",") if self.failed_attempts else []
        )
        attempts.append(str(int(timestamp)))
        self.failed_attempts = ",".join(attempts)

    def too_many_attempts(self, value, timestamp):
        """Compare number of failed attempts to <value>"""
        self.clean_attempts(timestamp)
        attempts = self.failed_attempts.split(",")
        return len(attempts) > value


class TemporaryLockout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
