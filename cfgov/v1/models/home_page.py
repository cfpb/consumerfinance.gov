from wagtail.wagtailadmin.edit_handlers import (
    ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailsearch import index

from v1.atomic_elements import atoms, molecules
from v1.models.base import CFGOVPage
from v1.util import ref


class HomePage(CFGOVPage):
    header = StreamField([
        ('info_unit', molecules.InfoUnit()),
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

    # Sets page to only be createable at the root
    parent_page_types = ['wagtailcore.Page']

    template = 'index.html'

    objects = PageManager()

    search_fields = CFGOVPage.search_fields + [index.SearchField('header')]

    is_searchable = True

    def get_category_name(self, category_icon_name):
        cats = dict(ref.limited_categories)
        return cats[str(category_icon_name)]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        return context
