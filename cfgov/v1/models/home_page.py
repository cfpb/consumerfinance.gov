from .base import CFGOVPage
from ..atomic_elements import atoms, molecules, organisms
from ..util import ref
from django.db import models
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel, FieldPanel, PageChooserPanel
from wagtail.wagtailcore import blocks


class HomePage(CFGOVPage):
    header = StreamField([
        ('half_width_link_blob', molecules.HalfWidthLinkBlob()),
    ], blank=True)

    latest_updates = StreamField([
        ('posts', blocks.ListBlock(blocks.StructBlock([
            ('categories', blocks.ChoiceBlock(choices=ref.limited_categories,
                                              required=False)),
            ('link', atoms.Hyperlink()),
            ('date', blocks.DateTimeBlock(required=False)),
        ]))),
    ], blank=True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('latest_updates'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    parent_page_types = ['wagtailcore.Page']  # Sets page to only be createable at the root

    template = 'index.html'

    objects = PageManager()

    def get_category_name(self, category_icon_name):
        cats = dict(ref.limited_categories)
        return cats[str(category_icon_name)]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        return context
