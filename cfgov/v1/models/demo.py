from django.db import models

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, \
    FieldRowPanel, TabbedInterface, ObjectList, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailcore import blocks

from .base import CFGOVPage
from .molecules import HalfWidthLinkBlob, TextIntroduction, ImageText5050
from .organisms import Well


class DemoPage(CFGOVPage):
    molecules = StreamField([
        ('half_width_link_blob', HalfWidthLinkBlob()),
        ('text_introduction', TextIntroduction()),
        ('image_text_5050', ImageText5050())
    ], blank=True)

    organisms = StreamField([
        ('well', Well())
    ], blank=True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('molecules'),
        StreamFieldPanel('organisms'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.promote_panels, heading='Promote'),
        ObjectList(CFGOVPage.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request):
        context = super(DemoPage, self).get_context(request)
        return context

    def get_template(self, request):
        return 'v1/demo/index.html'
