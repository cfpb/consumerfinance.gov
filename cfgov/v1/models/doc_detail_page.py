import itertools

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import PAGE_TEMPLATE_VAR

from .base import CFGOVPage
from . import molecules
from . import organisms


class DocumentDetailPage(CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('item_introduction', organisms.ItemIntroduction()),
    ], blank=True)

    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', molecules.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table', organisms.Table()),
    ], blank=True)

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

    template = 'document-detail/index.html'

    def elements(self):
        return list(itertools.chain(self.content.stream_data))
