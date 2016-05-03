from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import PAGE_TEMPLATE_VAR

from .base import CFGOVPage
from ..atomic_elements import molecules, organisms


class LandingPage(CFGOVPage):
    header = StreamField([
        ('hero', molecules.Hero()),
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)

    content = StreamField([
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('image_text_50_50_group', organisms.ImageText5050Group()),
        ('half_width_link_blob_group', organisms.HalfWidthLinkBlobGroup()),
        ('well', organisms.Well()),
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

    def get_context(self, request, *args, **kwargs):
        return {
            PAGE_TEMPLATE_VAR: self,
            'self': self,
            'request': request,
        }

    template = 'landing-page/index.html'
