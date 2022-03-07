from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, PageManager
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel

from flags.state import flag_enabled
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from v1.atomic_elements import atoms, molecules, organisms
from v1.models.base import CFGOVPage


class HomePageContentBlock(blocks.StreamBlock):
    jumbo_hero = molecules.JumboHero()
    features = organisms.InfoUnitGroup()

    class Meta:
        block_counts = {
            "jumbo_hero": {"max_num": 1},
            "features": {"max_num": 1},
        }


class HighlightCardValue(blocks.StructValue):
    @property
    def link_text(self):
        return _("Read more")

    @property
    def card_type(self):
        return 'highlight'


class HighlightCardBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    text = blocks.TextBlock(required=False)
    link_url = atoms.URLOrRelativeURLBlock()

    class Meta:
        value_class = HighlightCardValue


class HighlightCardStreamBlock(blocks.StreamBlock):
    highlight = HighlightCardBlock()


class AnswerPageStreamBlock(blocks.StreamBlock):
    page = blocks.PageChooserBlock(page_type="ask_cfpb.AnswerPage")


def image_passthrough(image, *args, **kwargs):
    """Passthrough replacement for Wagtail {{ image }} tag.

    This is needed because, as written, the hero module template assumes that
    it will get passed a Wagtail image object, which needs to get converted
    into e.g. a URL to render. We want to pass the hero module a URL directly.
    """
    return image


class HomePage(CFGOVPage):
    content = StreamField(HomePageContentBlock(), blank=True)

    card_heading = models.CharField(max_length=40, null=True, blank=True)

    answer_page_links = StreamField(AnswerPageStreamBlock, blank=True)
    highlight_cards = StreamField(HighlightCardStreamBlock, blank=True)

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList([StreamFieldPanel("content")], heading="Content"),
            ObjectList(
                [
                    InlinePanel(
                        "info_units", min_num=3, max_num=6, label="Info Unit"
                    ),
                ],
                heading="Info Units",
            ),
            ObjectList(
                [
                    FieldPanel("card_heading"),
                    InlinePanel("cards", min_num=3, max_num=3, label="Card"),
                ],
                heading="Cards",
            ),
            ObjectList(
                CFGOVPage.content_panels
                + [
                    StreamFieldPanel("answer_page_links"),
                    StreamFieldPanel("highlight_cards"),
                ],
                heading="Content (2021)",
            ),
            ObjectList(CFGOVPage.settings_panels, heading="Configuration"),
        ]
    )

    objects = PageManager()

    def get_context(self, request):
        context = super().get_context(request)

        context.update(
            {
                "info_units": [
                    info_unit.as_info_unit()
                    for info_unit in self.info_units.select_related("image")
                ],
                "card_heading": self.card_heading,
                "cards": self.cards.all(),
                "image_passthrough": image_passthrough,
            }
        )

        return context

    def get_template(self, request, *args, **kwargs):
        preview_mode = getattr(request, 'preview_mode', None)

        if preview_mode is None:
            if flag_enabled('HOME_PAGE_2021', request=request):
                preview_mode = 'home_page_2021'
            else:
                preview_mode = ''

        templates = {
            '': 'v1/home_page/home_page.html',
            'home_page_2021': 'v1/home_page/home_page_2021.html',
        }

        return templates[preview_mode]

    @property
    def preview_modes(self):
        return super().preview_modes + [('home_page_2021', '2021 version')]

    def serve_preview(self, request, mode_name):
        # TODO: Remove this once we are on Wagtail 2.5+.
        # Implemented in Wagtail core in
        # https://github.com/wagtail/wagtail/pull/7596
        request.preview_mode = mode_name
        return super().serve_preview(request, mode_name)


class HomePageInfoUnit(Orderable, ClusterableModel):
    page = ParentalKey(
        "v1.HomePage", on_delete=models.CASCADE, related_name="info_units"
    )
    title = models.CharField(
        max_length=35,
        help_text=(
            "35 characters maximum (including spaces). "
            "Sentence case, unless proper noun."
        ),
    )
    body = models.TextField(
        max_length=140,
        help_text=("140 characters maximum (including spaces)."),
    )
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("body"),
        ImageChooserPanel("image"),
        # Note: this min_num=1 doesn't seem to work properly, allowing users to
        # save new info units without providing links. This might be due to the
        # incomplete support for nested InlinePanels in our version of Wagtail.
        # See comments above and https://github.com/wagtail/wagtail/pull/5566.
        InlinePanel("links", min_num=1, label="Link"),
    ]

    def as_info_unit(self):
        """Convert model instance into data for molecules.InfoUnit.

        This allows us to use the existing InfoUnit template to render this
        model instance.
        """
        return {
            "image": {
                "upload": self.image,
            },
            "heading": {
                "text": self.title,
                "level": "h2",
                "level_class": "h3",
            },
            "body": self.body,
            "links": [
                {
                    "text": link.text,
                    "url": link.url,
                }
                for link in self.links.all()
            ],
        }


class HomePageInfoUnitLink(Orderable):
    info_unit = ParentalKey(
        "v1.HomePageInfoUnit", on_delete=models.CASCADE, related_name="links"
    )
    text = models.CharField(
        max_length=40, help_text=("40 characters maximum (including spaces).")
    )
    # TODO: Change this to use a URLField that also allows relative links.
    # https://code.djangoproject.com/ticket/10896
    url = models.CharField("URL", max_length=255)

    panels = [
        FieldPanel("text"),
        FieldPanel("url"),
    ]


# Deprecated
class HomePageCard(Orderable):
    @property
    def card_type(self):
        return 'featured'

    page = ParentalKey(
        "v1.HomePage", on_delete=models.CASCADE, related_name="cards"
    )
    icon = models.CharField(
        max_length=64,
        help_text=mark_safe(
            "<a href="
            '"https://cfpb.github.io/design-system/foundation/iconography"'
            ">See full list of icon names.</a>"
        ),
    )
    text = models.TextField(
        max_length=100,
        help_text=("100 characters maximum (including spaces)."),
    )
    link_text = models.CharField(
        max_length=25, help_text=("25 characters maximum (including spaces).")
    )
    # TODO: Change this to use a URLField that also allows relative links.
    link_url = models.CharField("Link URL", max_length=255)

    panels = [
        FieldPanel("icon"),
        FieldPanel("text"),
        FieldPanel("link_text"),
        FieldPanel("link_url"),
    ]
