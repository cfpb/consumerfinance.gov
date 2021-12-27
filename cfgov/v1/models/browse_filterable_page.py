from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager
from wagtail.search import index

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.documents import (
    EnforcementActionFilterablePagesDocumentSearch,
    EventFilterablePagesDocumentSearch
)
from v1.models.base import CFGOVPage
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.models.filterable_list_mixins import (
    CategoryFilterableMixin, FilterableListMixin
)
from v1.models.learn_page import EventPage


NEWSROOM_CACHE_TAG = "newsroom"


class BrowseFilterableContent(StreamBlock):
    """Defines the StreamField blocks for BrowseFilterablePage content.

    Pages can have at most one filterable list.
    """
    full_width_text = organisms.FullWidthText()
    filter_controls = organisms.FilterableList()
    feedback = v1_blocks.Feedback()

    class Meta:
        block_counts = {
            'filter_controls': {'max_num': 1},
        }


class BrowseFilterablePage(FilterableListMixin, CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', organisms.FeaturedContent()),
    ])
    content = StreamField(BrowseFilterableContent)

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

    search_fields = CFGOVPage.search_fields + [
        index.SearchField('content'),
        index.SearchField('header')
    ]

    @property
    def page_js(self):
        return (
            super(BrowseFilterablePage, self).page_js
            + ['secondary-navigation.js']
        )


class EnforcementActionsFilterPage(BrowseFilterablePage):
    template = 'browse-filterable/index.html'
    objects = PageManager()

    @staticmethod
    def get_form_class():
        from .. import forms
        return forms.EnforcementActionsFilterForm

    @staticmethod
    def get_model_class():
        return EnforcementActionPage

    @staticmethod
    def get_search_class():
        return EnforcementActionFilterablePagesDocumentSearch


class EventArchivePage(BrowseFilterablePage):
    template = 'browse-filterable/index.html'

    objects = PageManager()

    @staticmethod
    def get_model_class():
        return EventPage

    @staticmethod
    def get_form_class():
        from .. import forms
        return forms.EventArchiveFilterForm

    @staticmethod
    def get_search_class():
        return EventFilterablePagesDocumentSearch


class NewsroomLandingPage(CategoryFilterableMixin, BrowseFilterablePage):
    template = 'newsroom/index.html'
    filterable_categories = ['Newsroom']

    objects = PageManager()

    def serve(self, request, *args, **kwargs):
        response = super().serve(request, *args, **kwargs)
        response['Edge-Cache-Tag'] = NEWSROOM_CACHE_TAG
        return response
