from wagtail.wagtailadmin.edit_handlers import (
    ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailsearch import index

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.feeds import FilterableFeedPageMixin
from v1.models.base import CFGOVPage
from v1.util.filterable_list import FilterableListMixin


class SublandingFilterablePage(FilterableFeedPageMixin,
                               FilterableListMixin,
                               CFGOVPage):
    header = StreamField([
        ('hero', molecules.Hero()),
    ], blank=True)
    content = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('full_width_text', organisms.FullWidthText()),
        ('filter_controls', organisms.FilterableList()),
        ('featured_content', organisms.FeaturedContent()),
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

    search_fields = CFGOVPage.search_fields + [
        index.SearchField('content'),
        index.SearchField('header')
    ]


class ActivityLogPage(SublandingFilterablePage):
    template = 'activity-log/index.html'
    filterable_categories = ('Blog', 'Newsroom', 'Research Report')
    filterable_children_only = False
    filterable_per_page_limit = 100

    objects = PageManager()
