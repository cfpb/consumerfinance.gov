from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList
from wagtail.wagtailcore.models import PageManager

from v1.models.base import CFGOVPage
from v1.models.learn_page import AbstractFilterPage
from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from ..feeds import FilterableFeedPageMixin
from v1.util.filterable_list import FilterableListMixin


class SublandingFilterablePage(FilterableFeedPageMixin, FilterableListMixin, CFGOVPage):
    header = StreamField([
        ('hero', molecules.Hero()),
    ], blank=True)
    content = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('full_width_text', organisms.FullWidthText()),
        ('filter_controls', organisms.FilterControls()),
        ('featured_content', molecules.FeaturedContent()),
        ('feedback', v1_blocks.Feedback()),
    ])

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

    template = 'sublanding-page/index.html'

    objects = PageManager()


class ActivityLogPage(SublandingFilterablePage):
    template = 'activity-log/index.html'

    objects = PageManager()

    def base_query(self, hostname):
        return AbstractFilterPage.objects.live_shared(hostname)

    def per_page_limit(self):
        return 100
