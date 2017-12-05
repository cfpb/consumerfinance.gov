import itertools

from wagtail.wagtailadmin.edit_handlers import (
    ObjectList,
    StreamFieldPanel,
    TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.feeds import FilterableFeedPageMixin
from v1.models.base import CFGOVPage
from v1.models.learn_page import AbstractFilterPage
from v1.util import ref
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

    @classmethod
    def eligible_categories(cls):
        categories = dict(ref.categories)
        return sorted(itertools.chain(*(
            dict(categories[category]).keys()
            for category in ('Blog', 'Newsroom', 'Research Report')
        )))

    @classmethod
    def base_query(cls):
        """
        Recent updates pages should only show content from certain categories.
        """
        eligible_pages = AbstractFilterPage.objects.live()

        return eligible_pages.filter(
            categories__name__in=cls.eligible_categories()
        )

    def per_page_limit(self):
        return 100
