from django.db import models

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager
from wagtail.wagtailsearch import index

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules, organisms
from v1.feeds import FilterableFeedPageMixin
from v1.models.base import CFGOVPage
from v1.util.filterable_list import FilterableListMixin


class BrowseFilterablePage(FilterableFeedPageMixin,
                           FilterableListMixin,
                           CFGOVPage):
    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
        ('featured_content', organisms.FeaturedContent()),
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


class EventArchivePage(BrowseFilterablePage):
    template = 'browse-filterable/index.html'

    objects = PageManager()

    @staticmethod
    def get_form_class():
        from .. import forms
        return forms.EventArchiveFilterForm


class NewsroomLandingPage(BrowseFilterablePage):
    template = 'newsroom/index.html'
    filterable_categories = ('Blog', 'Newsroom')
    filterable_children_only = False

    objects = PageManager()
