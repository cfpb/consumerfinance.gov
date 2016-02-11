from itertools import chain

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from .base import CFGOVPage
from . import molecules
from . import organisms


class SublandingPage(CFGOVPage):
    header = StreamField([
        ('hero', molecules.Hero()),
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)
    content = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', molecules.FeaturedContent()),
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('image_text_50_50_group', organisms.ImageText5050Group()),
        ('full_width_text', organisms.FullWidthText()),
        ('half_width_link_blob_group', organisms.HalfWidthLinkBlobGroup()),
        ('post_preview_snapshot', organisms.PostPreviewSnapshot()),
        ('well', organisms.Well()),
        ('table', organisms.Table()),
        ('contact', organisms.MainContactInfo()),
        ('formfield_with_button', molecules.FormFieldWithButton()),
    ], blank=True)
    sidebar_breakout = StreamField([
        ('slug', blocks.CharBlock(icon='title')),
        ('heading', blocks.CharBlock(icon='title')),
        ('paragraph', blocks.RichTextBlock(icon='edit')),
        ('breakout_image', blocks.StructBlock([
            ('image', ImageChooserBlock()),
            ('is_round', blocks.BooleanBlock(required=False, default=True,
                                             label='Round?')),
            ('icon', blocks.CharBlock(help_text='Enter icon class name.')),
            ('heading', blocks.CharBlock(label='Introduction Heading')),
            ('body', blocks.TextBlock(label='Introduction Body')),
        ], heading='Breakout Image', icon='image')),
        ('related_posts', organisms.RelatedPosts()),
    ], blank=True)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    sidebar_panels = [
        StreamFieldPanel('sidebar_breakout'),
    ] + CFGOVPage.sidefoot_panels

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(sidebar_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'sublanding-page/index.html'

    def get_browsefilterable_posts(self, request):
        filter_pages = [p.specific for p in self.get_descendants()
                        if 'BrowseFilterablePage' in p.specific_class.__name__]
        posts = []
        for page in filter_pages:
            form_class = page.get_form_class()
            posts.append(page.get_page_set(form_class(parent=page),
                                           request.site.hostname))
        return sorted(list(chain(*posts)))
