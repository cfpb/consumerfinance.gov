from django.db import models
from django.utils.safestring import mark_safe

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, PageManager
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage


class HomePageContentBlock(StreamBlock):
    jumbo_hero = molecules.JumboHero()
    features = organisms.InfoUnitGroup()

    class Meta:
        block_counts = {
            'jumbo_hero': {'max_num': 1},
            'features': {'max_num': 1},
        }


class HomePage(CFGOVPage):
    content = StreamField(HomePageContentBlock, blank=True)

    card_heading = models.CharField(max_length=40, null=True, blank=True)

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList([StreamFieldPanel('content')], heading='Content'),
        ObjectList([
            InlinePanel(
                'info_units', min_num=3, max_num=6, label="Info Unit"
            ),
        ], heading='Info Units'),
        ObjectList([
            FieldPanel('card_heading'),
            InlinePanel('cards', min_num=3, max_num=3, label="Card"),
        ], heading='Cards'),
        ObjectList(
            # The only general content panel is the page title, which isn't
            # displayed or used except for slug generation in Wagtail. For this
            # reason it lives on the configuration tab so that it doesn't
            # require a tab of its own.
            CFGOVPage.content_panels + CFGOVPage.settings_panels,
            heading='Configuration'
        ),
    ])

    # Sets page to only be createable at the root
    parent_page_types = ['wagtailcore.Page']

    objects = PageManager()

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        context.update({
            'info_units': [
                info_unit.as_info_unit()
                for info_unit in
                self.info_units.select_related('image')
            ],
            'card_heading': self.card_heading,
            'cards': self.cards.all(),
        })

        return context


class HomePageInfoUnit(Orderable, ClusterableModel):
    page = ParentalKey(
        'v1.HomePage', on_delete=models.CASCADE, related_name='info_units'
    )
    title = models.CharField(max_length=35, help_text=(
        "35 characters maximum (including spaces). "
        "Sentence case, unless proper noun."
    ))
    body = models.TextField(max_length=140, help_text=(
        "140 characters maximum (including spaces)."
    ))
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
        ImageChooserPanel('image'),
        # Note: this min_num=1 doesn't seem to work properly, allowing users to
        # save new info units without providing links. This might be due to the
        # incomplete support for nested InlinePanels in our version of Wagtail.
        # See comments above and https://github.com/wagtail/wagtail/pull/5566.
        InlinePanel('links', min_num=1, label="Link"),
    ]

    def as_info_unit(self):
        """Convert model instance into data for molecules.InfoUnit.

        This allows us to use the existing InfoUnit template to render this
        model instance.
        """
        return {
            'image': {
                'upload': self.image,
            },
            'heading': {
                'text': self.title,
                'level': 'h2',
                'level_class': 'h3',
            },
            'body': self.body,
            'links': [
                {
                    'text': link.text,
                    'url': link.url,
                } for link in self.links.all()
            ],
        }


class HomePageInfoUnitLink(Orderable):
    info_unit = ParentalKey(
        'v1.HomePageInfoUnit', on_delete=models.CASCADE, related_name='links'
    )
    text = models.CharField(max_length=40, help_text=(
        "40 characters maximum (including spaces)."
    ))
    # TODO: Change this to use a URLField that also allows relative links.
    # https://code.djangoproject.com/ticket/10896
    url = models.CharField("URL", max_length=255)

    panels = [
        FieldPanel('text'),
        FieldPanel('url'),
    ]


class HomePageCard(Orderable):
    page = ParentalKey(
        'v1.HomePage', on_delete=models.CASCADE, related_name='cards'
    )
    icon = models.CharField(max_length=64, help_text=mark_safe(
        '<a href='
        '"https://cfpb.github.io/design-system/foundation/iconography"'
        '>See full list of icon names.</a>'
    ))
    text = models.TextField(max_length=100, help_text=(
        "100 characters maximum (including spaces)."
    ))
    link_text = models.CharField(max_length=25, help_text=(
        "25 characters maximum (including spaces)."
    ))
    # TODO: Change this to use a URLField that also allows relative links.
    link_url = models.CharField("Link URL", max_length=255)

    panels = [
        FieldPanel('icon'),
        FieldPanel('text'),
        FieldPanel('link_text'),
        FieldPanel('link_url'),
    ]
