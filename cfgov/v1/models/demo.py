from django.db import models

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from .base import CFGOVPage
from . import atoms
from . import molecules
from . import organisms
from .snippets import Contact


class DemoPage(CFGOVPage):
    molecules = StreamField([
        ('number', atoms.NumberBlock()),
        ('half_width_link_blob', molecules.HalfWidthLinkBlob()),
        ('text_introduction', molecules.TextIntroduction()),
        ('image_text_2575', molecules.ImageText2575()),
        ('image_text_5050', molecules.ImageText5050()),
        ('hero', molecules.Hero()),
        ('formfield_with_button', molecules.FormFieldWithButton()),
        ('call_to_action', molecules.CallToAction()),
        ('expandable', molecules.Expandable()),
        ('featured_content', molecules.FeaturedContent()),

    ], blank=True)

    organisms = StreamField([
        ('well', organisms.Well()),
        ('full_width_text', organisms.FullWidthText()),
        ('post_preview', organisms.PostPreview()),
        ('expandable_group', organisms.ExpandableGroup()),
        ('item_intro', organisms.ItemIntroduction()),
    ], blank=True)

    contact = models.ForeignKey(
        Contact,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('molecules'),
        StreamFieldPanel('organisms'),
        SnippetChooserPanel('contact'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(CFGOVPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Settings',
                   classname="settings"),
    ])

    def get_context(self, request):
        context = super(DemoPage, self).get_context(request)
        return context

    def get_template(self, request):
        return 'wagtail/demo/index.html'
