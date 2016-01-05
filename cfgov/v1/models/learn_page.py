import itertools

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import PAGE_TEMPLATE_VAR

from .base import CFGOVPage
from . import molecules
from . import organisms


class LearnPage(CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)

    content = StreamField([
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('well', organisms.Well()),
        ('full_width_text', organisms.FullWidthText()),
        ('expandable', molecules.Expandable()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('table', organisms.Table()),
        ('call_to_action', molecules.CallToAction()),
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

    template = 'learn-page/index.html'

    def elements(self):
        return list(itertools.chain(self.content.stream_data))
