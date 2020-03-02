from django.db import models
from django.utils.safestring import mark_safe

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from v1.models.base import CFGOVPage


try:
    from wagtail.admin.edit_handlers import (
        FieldPanel, InlinePanel, ObjectList, TabbedInterface
    )
    from wagtail.admin.forms import (
        WagtailAdminModelFormMetaclass, WagtailAdminPageForm
    )
    from wagtail.core.models import Orderable, PageManager
    from wagtail.images import get_image_model_string
    from wagtail.images.edit_handlers import ImageChooserPanel
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    from wagtail.wagtailadmin.edit_handlers import (
        FieldPanel, InlinePanel, ObjectList, TabbedInterface
    )
    from wagtail.wagtailadmin.forms import (
        WagtailAdminModelFormMetaclass, WagtailAdminPageForm
    )
    from wagtail.wagtailcore.models import Orderable, PageManager
    from wagtail.wagtailimages import get_image_model_string
    from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


# These classes are used to add support for nested InlinePanels, and are
# referenced by HomePage.base_form_class. This workaround comes from
# https://github.com/wagtail/wagtail/issues/5511. Proper support for nested
# inline panels in Wagtail won't be added until version 2.8, see
# https://github.com/wagtail/wagtail/pull/5566.
class HomePageFormMetaclass(WagtailAdminModelFormMetaclass):
    @classmethod
    def child_form(cls):
        return HomePageForm


class HomePageForm(WagtailAdminPageForm, metaclass=HomePageFormMetaclass):
    pass


class HomePage(CFGOVPage):
    card_heading = models.CharField(max_length=40, null=True, blank=True)

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList([
            InlinePanel(
                'carousel_items', min_num=4, max_num=4, label="Carousel Item"
            ),
        ], heading='Carousel'),
        ObjectList([
            InlinePanel(
                'info_units', min_num=6, max_num=6, label="Info Unit"
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

    base_form_class = HomePageForm

    @property
    def page_js(self):
        return super(HomePage, self).page_js + ['home-page.js']

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        context.update({
            'carousel_items': self.carousel_items.select_related('image'),
            'info_units': [
                info_unit.as_info_unit()
                for info_unit in
                self.info_units.select_related('image')
            ],
            'card_heading': self.card_heading,
            'cards': self.cards.all(),
        })

        return context


class HomePageCarouselItem(Orderable):
    page = ParentalKey(
        'v1.HomePage', on_delete=models.CASCADE, related_name='carousel_items'
    )
    title = models.CharField(max_length=45, help_text=(
        "45 characters maximum (including spaces). "
        "Sentence case, unless proper noun."
    ))
    body = models.TextField(max_length=160, help_text=(
        "160 characters maximum (including spaces)."
    ))
    link_text = models.CharField(max_length=35, help_text=(
        "35 characters maximum (including spaces). "
        "Lead with a verb, and be specific."
    ))
    # TODO: Change this to use a URLField that also allows relative links.
    # https://code.djangoproject.com/ticket/10896
    link_url = models.CharField("Link URL", max_length=255)
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
        FieldPanel('link_text'),
        FieldPanel('link_url'),
        ImageChooserPanel('image'),
    ]


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
            'heading': '<h3>%s</h3>' % self.title,
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
