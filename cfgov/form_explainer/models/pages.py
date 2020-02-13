from django.core.exceptions import ValidationError

from wagtail.wagtailadmin.edit_handlers import (
    ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.blocks import StreamBlockValidationError
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailsearch import index

from form_explainer.models.blocks import Explainer

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.models.base import CFGOVPage, CFGOVPageManager


def validate_explainer_count(value):
    block_types = [
        data.block_type for data in value
    ]
    if block_types.count('explainer') > 1:
        raise StreamBlockValidationError(
            non_block_errors=ValidationError(
                'Only one explainer block is allowed on this page.',
                code='invalid',
            )
        )


class FormExplainerPage(CFGOVPage):
    header = StreamField([
        ('hero', molecules.Hero()),
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)

    content = StreamField([
        ('explainer', Explainer()),
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('well', organisms.Well()),
        ('feedback', v1_blocks.Feedback()),
    ], blank=True, validators=[validate_explainer_count])

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'form-explainer/index.html'

    objects = CFGOVPageManager()

    search_fields = CFGOVPage.search_fields + [
        index.SearchField('header')
    ]
