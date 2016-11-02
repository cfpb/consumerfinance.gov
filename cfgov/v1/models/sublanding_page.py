from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList, \
    StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailimages.blocks import ImageChooserBlock

from .base import CFGOVPage
from .. import blocks as v1_blocks
from ..atomic_elements import molecules, organisms
from ..util import util
from jobmanager.models import JobListingList
from v1.forms import FilterableListForm


class SublandingPage(CFGOVPage):
    header = StreamField([
        ('hero', molecules.Hero()),
    ], blank=True)
    content = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', molecules.FeaturedContent()),
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('image_text_50_50_group', organisms.ImageText5050Group()),
        ('full_width_text', organisms.FullWidthText()),
        ('half_width_link_blob_group', organisms.HalfWidthLinkBlobGroup()),
        ('third_width_link_blob_group', organisms.ThirdWidthLinkBlobGroup()),
        ('post_preview_snapshot', organisms.PostPreviewSnapshot()),
        ('well', organisms.Well()),
        ('table', organisms.Table(editable=False)),
        ('table_block', organisms.AtomicTableBlock(table_options={'renderer': 'html'})),
        ('contact', organisms.MainContactInfo()),
        ('formfield_with_button', molecules.FormFieldWithButton()),
        ('reg_comment', organisms.RegComment()),
        ('feedback', v1_blocks.Feedback()),
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
            ('heading', blocks.CharBlock(required=False, label='Introduction Heading')),
            ('body', blocks.TextBlock(required=False, label='Introduction Body')),
        ], heading='Breakout Image', icon='image')),
        ('related_posts', organisms.RelatedPosts()),
        ('job_listing_list', JobListingList()),
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

    objects = PageManager()

    def get_browsefilterable_posts(self, request, limit):
        filter_pages = [p.specific for p in self.get_appropriate_descendants(request.site.hostname)
                        if 'FilterablePage' in p.specific_class.__name__
                        and 'archive' not in p.title.lower()]
        posts_tuple_list = []
        for page in filter_pages:
            form_id = str(page.form_id())
            form = FilterableListForm(parent=page, hostname=request.site.hostname)
            for post in form.get_page_set():
                posts_tuple_list.append((form_id, post))
        return sorted(posts_tuple_list, key=lambda p: p[1].date_published, reverse=True)[:limit]
