import itertools

from django.db import models
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, ObjectList,
                                                StreamFieldPanel,
                                                TabbedInterface)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.feeds import FilterableFeedPageMixin
from v1.models.base import CFGOVPage
from v1.models.learn_page import AbstractFilterPage
from v1.util import ref
from v1.util.filterable_list import FilterableListMixin


class BrowseFilterablePage(FilterableFeedPageMixin, FilterableListMixin,
                           CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', molecules.FeaturedContent()),
    ])
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('filter_controls', organisms.FilterControls()),
        ('feedback', v1_blocks.Feedback()),
    ])

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    # General content tab
    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel('secondary_nav_exclude_sibling_pages'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='SideFoot'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    template = 'browse-filterable/index.html'

    objects = PageManager()

    def add_page_js(self, js):
        super(BrowseFilterablePage, self).add_page_js(js)
        js['template'] += ['secondary-navigation.js']


class EventArchivePage(BrowseFilterablePage):
    template = 'browse-filterable/index.html'

    objects = PageManager()

    @staticmethod
    def get_form_class():
        from .. import forms
        return forms.EventArchiveFilterForm


class NewsroomLandingPage(BrowseFilterablePage):
    template = 'newsroom/index.html'

    objects = PageManager()

    @classmethod
    def eligible_categories(cls):
        categories = dict(ref.categories)
        return sorted(itertools.chain(*(
            dict(categories[category]).keys()
            for category in ('Blog', 'Newsroom')
        )))

    @classmethod
    def base_query(cls, hostname):
        """Newsroom pages should only show content from certain categories."""
        eligible_pages = AbstractFilterPage.objects.live_shared(hostname)

        return eligible_pages.filter(
            categories__name__in=cls.eligible_categories()
        )
