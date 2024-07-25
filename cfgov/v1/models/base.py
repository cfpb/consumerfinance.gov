import re
from operator import itemgetter

from django.conf import settings
from django.db import models
from django.db.models import F, Q, Value
from django.utils import translation
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.fields import StreamField
from wagtail.models import Page, Site

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.queryset import FakeQuerySet
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
        choices=sorted(settings.LANGUAGES, key=itemgetter(1)),
        default="en",
        max_length=100,
    )
    english_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="non_english_pages",
        help_text=(
            "Optionally select the English version of this page "
            "(non-English pages only)"
        ),
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
        FieldPanel("social_sharing_image"),
        FieldPanel("force_breadcrumbs", heading="Breadcrumbs"),
    ]

    sidefoot_panels = [
        FieldPanel("sidefoot"),
    ]

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(promote_panels, heading="Settings"),
        InlinePanel("categories", label="Categories", max_num=2),
        FieldPanel("tags", heading="Tags"),
        FieldPanel("authors", heading="Authors"),
        FieldPanel("content_owners", heading="Content Owners"),
        MultiFieldPanel(
            [
                FieldPanel("language", heading="Language"),
                FieldPanel("english_page"),
            ],
            "Translation",
        ),
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
        """Return page authors sorted alphabetically."""

        def sorting(name):
            parts = name.rsplit(" ", 1)
            return parts[0] if len(parts) == 1 else parts[1], parts[0]

        return sorted(
            [author.name for author in self.authors.all()], key=sorting
        )

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

        context["meta_description"] = self.get_meta_description()
        context["is_faq_page"] = self.is_faq_page()
        return context

    def _activate_translation(self, request):
        translation.activate(self.language)
        request.LANGUAGE_CODE = translation.get_language()

    def serve(self, request, *args, **kwargs):
        self._activate_translation(request)
        return super().serve(request, *args, **kwargs)

    def serve_preview(self, request, *args, **kwargs):
        self._activate_translation(request)
        return super().serve_preview(request, *args, **kwargs)

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
        return list(dict.fromkeys(self.page_js + self.streamfield_media("js")))

    # Returns the CSS files required by this page and its StreamField blocks.
    @property
    def media_css(self):
        return sorted(set(self.streamfield_media("css")))

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        return self.social_sharing_image

    def get_translations(self, inclusive=True, live=True):
        if self.language == "en" and self.pk:
            query = Q(english_page=self)
        elif self.english_page:
            query = Q(english_page=self.english_page) | Q(
                pk=self.english_page.pk
            )
        else:
            query = Q(pk__in=[])

        if self.pk:
            if inclusive:
                query = query | Q(pk=self.pk)
            else:
                query = query & ~Q(pk=self.pk)

        pages = CFGOVPage.objects.filter(query)

        if live:
            pages = pages.live()

        site = self.get_site()
        if site:
            pages = pages.in_site(site)

        if inclusive and not self.pk:

            def get_language_order(page):
                return list(dict(settings.LANGUAGES).keys()).index(
                    page.language
                )

            pages = FakeQuerySet(
                type(self),
                sorted(list(pages) + [self], key=get_language_order),
            )
        else:
            pages = pages.annotate(
                language_display_order=models.Case(
                    *[
                        models.When(language=language, then=i)
                        for i, language in enumerate(dict(settings.LANGUAGES))
                    ]
                ),
            ).order_by("language_display_order")

        return pages

    def get_translation_links(self, request, inclusive=True, live=True):
        language_names = dict(settings.LANGUAGES)

        return [
            {
                "href": translation.get_url(request=request),
                "language": translation.language,
                "text": language_names[translation.language],
            }
            for translation in self.get_translations(
                inclusive=inclusive, live=live
            )
        ]


class CFGOVPageCategory(models.Model):
    page = ParentalKey(CFGOVPage, related_name="categories")
    name = models.CharField(max_length=255, choices=ref.categories)

    class Meta:
        ordering = ["name"]

    panels = [
        FieldPanel("name"),
    ]
